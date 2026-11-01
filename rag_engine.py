"""A small, dependency-free agentic RAG engine for the CRAG Demo.

The local retriever uses deterministic feature-hashed TF-IDF-style vectors and a
lexical overlap signal. Web search is optional and only enabled when a Tavily
API key is configured. The engine deliberately prefers a grounded refusal over
an unsupported answer.
"""

from __future__ import annotations

import ast
import hashlib
import html
import json
import math
import os
import re
import threading
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable


_WORD_RE = re.compile(r"[a-zA-Z0-9]+(?:['’-][a-zA-Z0-9]+)?")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "by",
    "can", "could", "did", "do", "does", "for", "from", "had", "has",
    "have", "how", "i", "in", "into", "is", "it", "its", "may", "me",
    "might", "my", "of", "on", "or", "our", "please", "should", "that",
    "the", "their", "them", "there", "these", "this", "those", "to", "was",
    "we", "were", "what", "when", "where", "which", "who", "why", "will",
    "with", "would", "you", "your", "explain", "describe", "tell", "about",
}
_FRESHNESS_RE = re.compile(
    r"\b(latest|current|currently|today|tonight|right now|live|recent|recently|"
    r"this week|this month|this year|yesterday|tomorrow|weather|news|stock price|"
    r"exchange rate|release date|newest|202[4-9]|203\d)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    content: str
    source: str = "Knowledge base"
    url: str = ""


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    title: str
    text: str
    source: str
    url: str = ""


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float
    similarity: float
    lexical_coverage: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk.id,
            "document_id": self.chunk.document_id,
            "title": self.chunk.title,
            "text": self.chunk.text,
            "source": self.chunk.source,
            "url": self.chunk.url,
            "score": round(self.score, 4),
            "similarity": round(self.similarity, 4),
            "lexical_coverage": round(self.lexical_coverage, 4),
        }


class HashingEmbedder:
    """Produces normalized, sparse vectors without downloading a model."""

    def __init__(self, dimensions: int = 768) -> None:
        self.dimensions = dimensions

    @staticmethod
    def _normalize_word(word: str) -> str:
        word = word.casefold().replace("’", "'")
        irregular = {
            "retrieval": "retrieve", "retriever": "retrieve", "retrieves": "retrieve",
            "retrieved": "retrieve", "retrieving": "retrieve", "grounded": "ground",
            "grounding": "ground", "citations": "citation", "passages": "passage",
        }
        if word in irregular:
            return irregular[word]
        if len(word) > 4 and word.endswith("ies"):
            return word[:-3] + "y"
        if len(word) > 5 and word.endswith("ing"):
            stem = word[:-3]
            if len(stem) > 2 and stem[-1] == stem[-2]:
                stem = stem[:-1]
            return stem
        if len(word) > 4 and word.endswith("ed"):
            return word[:-2]
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            return word[:-1]
        return word

    @staticmethod
    def features(text: str) -> Counter[str]:
        meaningful = []
        for raw_word in _WORD_RE.findall(text):
            if raw_word.casefold() in _STOP_WORDS:
                continue
            word = HashingEmbedder._normalize_word(raw_word)
            if word not in _STOP_WORDS and len(word) > 1:
                meaningful.append(word)
        features: Counter[str] = Counter(meaningful)
        for left, right in zip(meaningful, meaningful[1:]):
            features[f"{left}_{right}"] += 0.55
        return features

    @staticmethod
    def query_terms(text: str) -> set[str]:
        terms = set()
        for raw_word in _WORD_RE.findall(text):
            if raw_word.casefold() in _STOP_WORDS:
                continue
            word = HashingEmbedder._normalize_word(raw_word)
            if word not in _STOP_WORDS and len(word) > 1:
                terms.add(word)
        return terms

    def embed(self, text: str) -> dict[int, float]:
        counts = self.features(text)
        vector: dict[int, float] = {}
        for feature, count in counts.items():
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] & 1 else -1.0
            vector[bucket] = vector.get(bucket, 0.0) + sign * (1.0 + math.log(float(count)))
        norm = math.sqrt(sum(value * value for value in vector.values()))
        if norm:
            vector = {index: value / norm for index, value in vector.items()}
        return vector


def _cosine_sparse(left: dict[int, float], right: dict[int, float]) -> float:
    if not left or not right:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    value = sum(weight * right.get(index, 0.0) for index, weight in left.items())
    return max(0.0, min(1.0, value))


def _split_document(document: Document, max_chars: int = 900, overlap: int = 120) -> list[Chunk]:
    text = re.sub(r"\r\n?", "\n", document.content).strip()
    if not text:
        return []

    blocks: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if not paragraph:
            continue
        if len(paragraph) <= max_chars:
            blocks.append(paragraph)
            continue
        sentences = [part.strip() for part in _SENTENCE_RE.split(paragraph) if part.strip()]
        current = ""
        for sentence in sentences:
            if len(sentence) > max_chars:
                if current:
                    blocks.append(current)
                    current = ""
                start = 0
                while start < len(sentence):
                    end = min(start + max_chars, len(sentence))
                    if end < len(sentence):
                        boundary = sentence.rfind(" ", start, end)
                        if boundary > start + max_chars // 2:
                            end = boundary
                    blocks.append(sentence[start:end].strip())
                    if end >= len(sentence):
                        break
                    start = max(start + 1, end - overlap)
                continue
            candidate = f"{current} {sentence}".strip()
            if current and len(candidate) > max_chars:
                blocks.append(current)
                current = sentence
            else:
                current = candidate
        if current:
            blocks.append(current)

    return [
        Chunk(
            id=f"{document.id}#{index + 1}",
            document_id=document.id,
            title=document.title,
            text=block,
            source=document.source,
            url=document.url,
        )
        for index, block in enumerate(blocks)
    ]


class VectorStore:
    """Thread-safe local vector index with a small hybrid lexical signal."""

    def __init__(self, documents: Iterable[Document] = ()) -> None:
        self._lock = threading.RLock()
        self._embedder = HashingEmbedder()
        self._documents: dict[str, Document] = {}
        self._chunks: list[Chunk] = []
        self._vectors: dict[str, dict[int, float]] = {}
        self.replace_documents(documents)

    def replace_documents(self, documents: Iterable[Document]) -> None:
        materialized = {document.id: document for document in documents}
        chunks: list[Chunk] = []
        vectors: dict[str, dict[int, float]] = {}
        for document in materialized.values():
            for chunk in _split_document(document):
                chunks.append(chunk)
                vectors[chunk.id] = self._embedder.embed(f"{chunk.title} {chunk.text}")
        with self._lock:
            self._documents = materialized
            self._chunks = chunks
            self._vectors = vectors

    def search(self, query: str, limit: int = 5) -> list[SearchHit]:
        query_vector = self._embedder.embed(query)
        query_terms = self._embedder.query_terms(query)
        if not query_vector:
            return []
        hits: list[SearchHit] = []
        with self._lock:
            chunks = tuple(self._chunks)
            vectors = dict(self._vectors)
        for chunk in chunks:
            similarity = _cosine_sparse(query_vector, vectors.get(chunk.id, {}))
            document_terms = self._embedder.query_terms(f"{chunk.title} {chunk.text}")
            coverage = (
                len(query_terms.intersection(document_terms)) / len(query_terms)
                if query_terms else 0.0
            )
            score = 0.76 * similarity + 0.24 * coverage
            hits.append(SearchHit(chunk, score, similarity, coverage))
        hits.sort(key=lambda hit: (hit.score, hit.lexical_coverage, hit.similarity), reverse=True)
        return hits[: max(1, min(int(limit), 20))]

    @property
    def document_count(self) -> int:
        with self._lock:
            return len(self._documents)

    @property
    def chunk_count(self) -> int:
        with self._lock:
            return len(self._chunks)

    def documents(self) -> list[Document]:
        with self._lock:
            return list(self._documents.values())


class ToolRegistry:
    """Registers JSON-schema-described tools and validates every invocation."""

    def __init__(self) -> None:
        self._tools: dict[str, tuple[dict[str, Any], Callable[[dict[str, Any]], dict[str, Any]]]] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        self._tools[name] = ({"name": name, "description": description, "parameters": parameters}, handler)

    def definitions(self) -> list[dict[str, Any]]:
        return [definition for definition, _ in self._tools.values()]

    def invoke(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        definition, handler = self._tools[name]
        schema = definition["parameters"]
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a JSON object.")
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = [key for key in required if key not in arguments]
        if missing:
            raise ValueError(f"Missing required tool argument(s): {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(arguments) - set(properties))
            if extras:
                raise ValueError(f"Unexpected tool argument(s): {', '.join(extras)}")
        for key, value in arguments.items():
            if key not in properties:
                continue
            expected = properties[key].get("type")
            if expected == "string" and not isinstance(value, str):
                raise ValueError(f"Tool argument '{key}' must be a string.")
            if expected == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
                raise ValueError(f"Tool argument '{key}' must be an integer.")
            if expected == "number" and (not isinstance(value, (int, float)) or isinstance(value, bool)):
                raise ValueError(f"Tool argument '{key}' must be a number.")
            if expected == "boolean" and not isinstance(value, bool):
                raise ValueError(f"Tool argument '{key}' must be a boolean.")
            allowed = properties[key].get("enum")
            if allowed is not None and value not in allowed:
                raise ValueError(f"Tool argument '{key}' must be one of: {', '.join(map(str, allowed))}.")
        return handler(arguments)


class TavilySearch:
    """Optional web-search adapter. No request is made unless configured."""

    ENDPOINT = "https://api.tavily.com/search"

    def __init__(self, api_key: str | None = None, timeout: float = 8.0) -> None:
        self.api_key = api_key if api_key is not None else os.getenv("TAVILY_API_KEY", "")
        self.timeout = timeout

    @property
    def configured(self) -> bool:
        return bool(self.api_key.strip())

    def search(self, query: str, max_results: int = 5) -> dict[str, Any]:
        if not self.configured:
            return {
                "available": False,
                "status": "not_configured",
                "message": "Web search is not configured. Set TAVILY_API_KEY to enable live search.",
                "results": [],
            }
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": max(1, min(int(max_results), 5)),
            "include_answer": False,
            "include_raw_content": False,
        }
        request = urllib.request.Request(
            self.ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read(1_500_000).decode("utf-8"))
            results = []
            for item in body.get("results", [])[:5]:
                url = str(item.get("url", ""))[:1000]
                title = str(item.get("title", "Untitled result"))[:300]
                content = re.sub(r"\s+", " ", str(item.get("content", ""))).strip()[:900]
                if content:
                    results.append({"title": title, "url": url, "content": content, "source": "Web search"})
            return {"available": True, "status": "ok", "results": results}
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            reason = getattr(error, "reason", None)
            message = "The web search provider could not be reached."
            if isinstance(reason, str) and reason:
                message = f"The web search provider could not be reached ({reason[:120]})."
            return {"available": False, "status": "error", "message": message, "results": []}


class AgentEngine:
    def __init__(
        self,
        documents: Iterable[Document],
        user_documents_path: str | Path | None = None,
        web_search: TavilySearch | None = None,
    ) -> None:
        self._seed_documents = {document.id: document for document in documents}
        self.user_documents_path = Path(user_documents_path) if user_documents_path else None
        self._user_documents: dict[str, Document] = {}
        self._data_lock = threading.RLock()
        self.web_search = web_search or TavilySearch()
        self._load_user_documents()
        self.store = VectorStore([*self._seed_documents.values(), *self._user_documents.values()])
        self.tools = ToolRegistry()
        self.tools.register(
            "calculator",
            "Safely evaluates a basic arithmetic expression using a restricted syntax tree.",
            {
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "Arithmetic expression."}},
                "required": ["expression"],
                "additionalProperties": False,
            },
            self._calculate,
        )
        self.tools.register(
            "web_search",
            "Searches the web through Tavily when TAVILY_API_KEY is configured.",
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Focused search query."},
                    "max_results": {"type": "integer", "description": "Maximum number of results (1-5)."},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            lambda args: self.web_search.search(args["query"], args.get("max_results", 5)),
        )

    @classmethod
    def from_json_files(
        cls,
        sample_documents_path: str | Path,
        user_documents_path: str | Path,
        web_search: TavilySearch | None = None,
    ) -> "AgentEngine":
        with Path(sample_documents_path).open("r", encoding="utf-8") as handle:
            raw_documents = json.load(handle)
        documents = [
            Document(
                id=str(item["id"]),
                title=str(item["title"]),
                content=str(item["content"]),
                source=str(item.get("source", "Knowledge base")),
                url=str(item.get("url", "")),
            )
            for item in raw_documents
        ]
        return cls(documents, user_documents_path, web_search)

    def _load_user_documents(self) -> None:
        path = self.user_documents_path
        if not path or not path.exists():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for item in data if isinstance(data, list) else []:
                if not isinstance(item, dict):
                    continue
                document = Document(
                    id=str(item.get("id", "")),
                    title=str(item.get("title", "")),
                    content=str(item.get("content", "")),
                    source="Uploaded",
                )
                if document.id.startswith("USER-") and document.title and document.content:
                    self._user_documents[document.id] = document
        except (OSError, json.JSONDecodeError, TypeError):
            self._user_documents = {}

    def _persist_user_documents(self) -> None:
        if not self.user_documents_path:
            return
        self.user_documents_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(document) for document in self._user_documents.values()]
        temporary = self.user_documents_path.with_suffix(self.user_documents_path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.user_documents_path)

    def add_document(self, title: str, content: str) -> dict[str, Any]:
        clean_title = re.sub(r"\s+", " ", str(title)).strip()[:240]
        clean_content = str(content).strip()
        if not clean_title:
            raise ValueError("A document title is required.")
        if len(clean_content) < 20:
            raise ValueError("Add at least 20 characters of document text.")
        if len(clean_content) > 100_000:
            raise ValueError("Documents must be 100,000 characters or fewer.")
        digest = hashlib.sha256(f"{clean_title}\n{clean_content}".encode("utf-8")).hexdigest()[:12]
        document = Document(
            id=f"USER-{digest}", title=clean_title, content=clean_content, source="Uploaded"
        )
        with self._data_lock:
            self._user_documents[document.id] = document
            self._persist_user_documents()
            self.store.replace_documents([*self._seed_documents.values(), *self._user_documents.values()])
        return self._document_summary(document)

    def delete_document(self, document_id: str) -> bool:
        if not document_id.startswith("USER-"):
            return False
        with self._data_lock:
            removed = self._user_documents.pop(document_id, None)
            if removed is None:
                return False
            self._persist_user_documents()
            self.store.replace_documents([*self._seed_documents.values(), *self._user_documents.values()])
            return True

    @staticmethod
    def _document_summary(document: Document) -> dict[str, Any]:
        return {
            "id": document.id,
            "title": document.title,
            "source": document.source,
            "characters": len(document.content),
        }

    def list_documents(self) -> list[dict[str, Any]]:
        documents = self.store.documents()
        documents.sort(key=lambda document: (document.source != "Knowledge base", document.title.casefold()))
        return [self._document_summary(document) for document in documents]

    @staticmethod
    def _calculate(arguments: dict[str, Any]) -> dict[str, Any]:
        expression = arguments["expression"]
        if len(expression) > 120:
            raise ValueError("The expression is too long.")
        normalized = expression.replace("^", "**")
        try:
            tree = ast.parse(normalized, mode="eval")
            value = AgentEngine._eval_math_node(tree.body)
        except (SyntaxError, ZeroDivisionError, OverflowError, ValueError) as error:
            raise ValueError(f"Unable to safely evaluate expression: {error}") from error
        if not math.isfinite(float(value)) or abs(value) > 1e18:
            raise ValueError("The result is outside the supported numeric range.")
        return {"expression": expression, "result": value, "formatted_result": AgentEngine._format_number(value)}

    @staticmethod
    def _eval_math_node(node: ast.AST) -> int | float:
        binary_ops: dict[type[ast.operator], Callable[[Any, Any], Any]] = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: a / b,
            ast.FloorDiv: lambda a, b: a // b,
            ast.Mod: lambda a, b: a % b,
            ast.Pow: lambda a, b: a ** b,
        }
        unary_ops: dict[type[ast.unaryop], Callable[[Any], Any]] = {
            ast.UAdd: lambda value: value,
            ast.USub: lambda value: -value,
        }
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            if abs(node.value) > 1e12:
                raise ValueError("A number is outside the supported range.")
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
            left = AgentEngine._eval_math_node(node.left)
            right = AgentEngine._eval_math_node(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 12:
                raise ValueError("Exponents must have an absolute value of 12 or less.")
            result = binary_ops[type(node.op)](left, right)
            if not isinstance(result, (int, float)) or abs(result) > 1e18:
                raise ValueError("An intermediate result is outside the supported range.")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
            return unary_ops[type(node.op)](AgentEngine._eval_math_node(node.operand))
        raise ValueError("Only numbers, parentheses, and +, -, *, /, //, %, and ^ are allowed.")

    @staticmethod
    def _format_number(value: int | float) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.10g}" if isinstance(value, float) else str(value)

    @staticmethod
    def _extract_expression(query: str) -> str | None:
        candidates = re.findall(r"[0-9\s().+\-*/%^]+", query)
        for candidate in candidates:
            candidate = candidate.strip().rstrip(".")
            if len(candidate) > 120 or not re.search(r"\d", candidate):
                continue
            if not re.search(r"[+\-*/%^]", candidate):
                continue
            try:
                ast.parse(candidate.replace("^", "**"), mode="eval")
                return candidate
            except SyntaxError:
                continue
        return None

    @staticmethod
    def _rewrite_query(query: str) -> str:
        synonyms = {
            "crag": "corrective retrieval augmented generation",
            "rag": "retrieval augmented generation",
            "vector": "embedding cosine similarity semantic search",
            "vectors": "embedding cosine similarity semantic search",
            "fallback": "external web search backup retrieval",
            "relevance": "evidence support quality relevance check",
            "grounding": "source evidence citations verification",
            "tool": "structured function calling JSON schema",
            "tools": "structured function calling JSON schema",
            "chunk": "passage document segment",
            "chunks": "passages document segments",
        }
        terms = [word.casefold() for word in _WORD_RE.findall(query) if word.casefold() not in _STOP_WORDS]
        expanded = list(terms)
        for term in terms:
            expansion = synonyms.get(term)
            if expansion:
                expanded.extend(expansion.split())
        # Keep the rewrite concise and deterministic while preserving the user's intent.
        return " ".join(dict.fromkeys(expanded)) or query.strip()

    @staticmethod
    def _is_relevant(hits: list[SearchHit]) -> bool:
        if not hits:
            return False
        best = hits[0]
        return best.score >= 0.19 and (best.lexical_coverage >= 0.24 or best.similarity >= 0.34)

    @staticmethod
    def _unique_hits(*groups: list[SearchHit], limit: int = 6) -> list[SearchHit]:
        hits: dict[str, SearchHit] = {}
        for group in groups:
            for hit in group:
                existing = hits.get(hit.chunk.id)
                if existing is None or hit.score > existing.score:
                    hits[hit.chunk.id] = hit
        return sorted(hits.values(), key=lambda hit: hit.score, reverse=True)[:limit]

    @staticmethod
    def _select_sentences(query: str, hits: list[SearchHit], limit: int = 3) -> list[tuple[str, SearchHit]]:
        terms = HashingEmbedder.query_terms(query)
        candidates: list[tuple[float, str, SearchHit]] = []
        seen: set[str] = set()
        primary_document = hits[0].chunk.document_id if hits else ""
        secondary_documents: set[str] = set()
        for hit in hits:
            is_primary = hit.chunk.document_id == primary_document
            if not is_primary:
                # Avoid padding a relevant answer with merely adjacent, low-scoring sources.
                if hit.score < 0.22 or (secondary_documents and hit.chunk.document_id not in secondary_documents):
                    continue
                secondary_documents.add(hit.chunk.document_id)
            sentences = [part.strip() for part in _SENTENCE_RE.split(hit.chunk.text) if part.strip()]
            if not sentences:
                sentences = [hit.chunk.text.strip()]
            for sentence in sentences:
                normalized = re.sub(r"\W+", " ", sentence.casefold()).strip()
                if not normalized or normalized in seen:
                    continue
                sentence_terms = HashingEmbedder.query_terms(sentence)
                overlap = len(terms.intersection(sentence_terms))
                score = hit.score + (overlap / max(len(terms), 1)) * 0.08
                if overlap == 0 and terms and not is_primary:
                    continue
                candidates.append((score, sentence, hit))
                seen.add(normalized)
        if not candidates:
            for hit in hits[:1]:
                sentence = hit.chunk.text.strip()
                if sentence:
                    candidates.append((hit.score, sentence, hit))
        candidates.sort(key=lambda item: item[0], reverse=True)
        return [(sentence, hit) for _, sentence, hit in candidates[:limit]]

    @staticmethod
    def _xml_document(text: str) -> str:
        return html.escape(text, quote=False)

    def _build_xml(
        self,
        reasoning_summary: str,
        sources: list[dict[str, Any]],
        answer: str,
    ) -> str:
        source_lines = []
        for source in sources:
            identifier = html.escape(str(source.get("id", "source")), quote=True)
            title = html.escape(str(source.get("title", "Source")), quote=True)
            url = html.escape(str(source.get("url", "")), quote=True)
            label = self._xml_document(str(source.get("title", "Source")))
            if url:
                source_lines.append(f'  <source id="{identifier}" title="{title}" url="{url}">{label}</source>')
            else:
                source_lines.append(f'  <source id="{identifier}" title="{title}">{label}</source>')
        if not source_lines:
            source_lines.append('  <source id="none">No supporting source was retrieved.</source>')
        return (
            "<reasoning>\n"
            f"  {self._xml_document(reasoning_summary)}\n"
            "</reasoning>\n\n"
            "<sources>\n"
            + "\n".join(source_lines)
            + "\n</sources>\n\n"
            "<answer>\n"
            f"  {self._xml_document(answer)}\n"
            "</answer>"
        )

    @staticmethod
    def _source_from_hit(hit: SearchHit) -> dict[str, Any]:
        return {
            "kind": "knowledge_base",
            "id": hit.chunk.document_id,
            "chunk_id": hit.chunk.id,
            "title": hit.chunk.title,
            "source": hit.chunk.source,
            "url": hit.chunk.url,
            "excerpt": hit.chunk.text,
            "score": round(hit.score, 4),
        }

    @staticmethod
    def _trace_step(stage: str, detail: str, status: str = "complete", **extra: Any) -> dict[str, Any]:
        return {"stage": stage, "detail": detail, "status": status, **extra}

    def query(self, query: str) -> dict[str, Any]:
        clean_query = re.sub(r"\s+", " ", str(query)).strip()
        if not clean_query:
            raise ValueError("Enter a question to start retrieval.")
        if len(clean_query) > 2_000:
            raise ValueError("Questions must be 2,000 characters or fewer.")

        started = time.perf_counter()
        expression = self._extract_expression(clean_query)
        needs_freshness = bool(_FRESHNESS_RE.search(clean_query))
        is_calculation = expression is not None and not needs_freshness
        if is_calculation:
            route = "direct_calculation"
            route_detail = "A numeric expression was detected; the calculator tool will verify the result."
        elif needs_freshness:
            route = "external_search"
            route_detail = "The question asks for time-sensitive information; live search will be attempted."
        else:
            route = "internal_knowledge_retrieval"
            route_detail = "The question will be checked against the local knowledge base first."

        trace: list[dict[str, Any]] = [
            self._trace_step("Query analysis", route_detail, route=route)
        ]
        sources: list[dict[str, Any]] = []
        tool_calls: list[dict[str, Any]] = []
        retrieval_passes: list[dict[str, Any]] = []
        relevant = False
        web_result: dict[str, Any] | None = None
        hits: list[SearchHit] = []
        calc_result: dict[str, Any] | None = None

        def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
            call_started = time.perf_counter()
            try:
                result = self.tools.invoke(name, arguments)
                status = str(result.get("status", "ok"))
            except (ValueError, TypeError, ArithmeticError) as error:
                result = {"status": "error", "message": str(error)}
                status = "error"
            call = {
                "name": name,
                "arguments": arguments,
                "status": status,
                "duration_ms": round((time.perf_counter() - call_started) * 1000, 2),
                "result": result,
            }
            tool_calls.append(call)
            return result

        if is_calculation and expression is not None:
            calc_result = call_tool("calculator", {"expression": expression})
            if calc_result.get("status") == "error":
                trace.append(self._trace_step("Structured tool call", "The calculator rejected the expression.", "warning", tool="calculator"))
            else:
                trace.append(
                    self._trace_step(
                        "Structured tool call",
                        f"Calculator evaluated {expression} safely.",
                        tool="calculator",
                        result=calc_result.get("formatted_result"),
                    )
                )
                sources.append({
                    "kind": "tool",
                    "id": "tool:calculator",
                    "title": "Verified calculator result",
                    "source": "Tool output",
                    "url": "",
                    "excerpt": f"{expression} = {calc_result.get('formatted_result')}",
                })
        else:
            retrieval_started = time.perf_counter()
            first_hits = self.store.search(clean_query, limit=5)
            relevant = self._is_relevant(first_hits)
            retrieval_passes.append({
                "query": clean_query,
                "result_count": len(first_hits),
                "top_score": round(first_hits[0].score, 4) if first_hits else 0.0,
                "relevant": relevant,
            })
            hits = first_hits if relevant else []
            trace.append(
                self._trace_step(
                    "Vector retrieval",
                    f"Searched {self.store.chunk_count} indexed chunks; "
                    + (f"best match scored {first_hits[0].score:.2f}." if first_hits else "the index returned no chunks."),
                    "complete" if relevant else "warning",
                    result_count=len(first_hits),
                    top_score=round(first_hits[0].score, 4) if first_hits else 0.0,
                    relevant=relevant,
                    duration_ms=round((time.perf_counter() - retrieval_started) * 1000, 2),
                )
            )

            if not relevant:
                rewritten = self._rewrite_query(clean_query)
                rewrite_started = time.perf_counter()
                second_hits = self.store.search(rewritten, limit=5)
                second_relevant = self._is_relevant(second_hits)
                retrieval_passes.append({
                    "query": rewritten,
                    "result_count": len(second_hits),
                    "top_score": round(second_hits[0].score, 4) if second_hits else 0.0,
                    "relevant": second_relevant,
                })
                hits = self._unique_hits(first_hits, second_hits)
                relevant = second_relevant or self._is_relevant(hits)
                trace.append(
                    self._trace_step(
                        "Query reformulation",
                        "Expanded key terms and retried local retrieval; "
                        + ("supporting context was found." if relevant else "local evidence is still weak."),
                        "complete" if relevant else "warning",
                        rewritten_query=rewritten,
                        result_count=len(second_hits),
                        top_score=round(second_hits[0].score, 4) if second_hits else 0.0,
                        relevant=second_relevant,
                        duration_ms=round((time.perf_counter() - rewrite_started) * 1000, 2),
                    )
                )

            should_search_web = needs_freshness or not relevant
            if should_search_web:
                search_query = clean_query if needs_freshness else self._rewrite_query(clean_query)
                web_result = call_tool("web_search", {"query": search_query, "max_results": 5})
                web_results = web_result.get("results", []) if isinstance(web_result, dict) else []
                configured = self.web_search.configured
                if web_results:
                    sources.extend({
                        "kind": "web",
                        "id": item.get("url") or f"web:{index + 1}",
                        "title": item.get("title", "Web result"),
                        "source": "Web search",
                        "url": item.get("url", ""),
                        "excerpt": item.get("content", ""),
                    } for index, item in enumerate(web_results))
                trace.append(
                    self._trace_step(
                        "Web search fallback",
                        (
                            f"Retrieved {len(web_results)} live result(s)." if web_results
                            else str(web_result.get("message", "No web results were returned."))
                        ),
                        "complete" if web_results else ("warning" if configured else "unavailable"),
                        tool="web_search",
                        configured=configured,
                        result_count=len(web_results),
                        query=search_query,
                        duration_ms=tool_calls[-1]["duration_ms"],
                    )
                )
            else:
                trace.append(self._trace_step("Evidence check", "Retrieved passages were judged relevant; no web fallback was needed."))

        web_results = (
            web_result.get("results", [])
            if isinstance(web_result, dict) and isinstance(web_result.get("results", []), list)
            else []
        )
        if is_calculation:
            if calc_result and calc_result.get("status") != "error":
                answer = f"{expression} evaluates to {calc_result['formatted_result']}."
            else:
                detail = calc_result.get("message", "The expression could not be evaluated safely.") if calc_result else "The expression could not be evaluated safely."
                answer = f"I cannot confirm this based on the available context. {detail}"
            reasoning_summary = "Classified as a direct calculation and passed the expression to a restricted arithmetic tool."
        elif needs_freshness:
            if web_results:
                result_phrases = [
                    f"{item.get('title', 'Search result')}: {item.get('content', '')} [{index + 1}]"
                    for index, item in enumerate(web_results[:3])
                    if item.get("content")
                ]
                answer = "Live search results: " + " ".join(result_phrases) if result_phrases else "I cannot confirm this based on the available context."
            else:
                answer = "I cannot confirm this based on the available context. The local knowledge base is not live, and web search did not return verifiable results."
            reasoning_summary = "Classified as time-sensitive, checked local retrieval, and attempted the configured web-search tool."
        elif web_results:
            result_phrases = [
                f"{item.get('title', 'Search result')}: {item.get('content', '')} [{index + 1}]"
                for index, item in enumerate(web_results[:3])
                if item.get("content")
            ]
            answer = "External search results: " + " ".join(result_phrases) if result_phrases else "I cannot confirm this based on the available context."
            reasoning_summary = "Local evidence remained insufficient after reformulation, so the web-search fallback was used."
        elif relevant:
            supporting = self._select_sentences(clean_query, hits, limit=3)
            sources_by_id = {source["id"]: source for source in sources}
            for _, hit in supporting:
                if hit.chunk.document_id not in sources_by_id:
                    source = self._source_from_hit(hit)
                    sources.append(source)
                    sources_by_id[hit.chunk.document_id] = source
            cited_sentences = [
                f"{sentence} [{hit.chunk.document_id}]"
                for sentence, hit in supporting
            ]
            answer = "Based on the indexed material: " + " ".join(cited_sentences) if cited_sentences else "I cannot confirm this based on the available context."
            best_score = max((hit.score for hit in hits), default=0.0)
            reasoning_summary = (
                f"Classified as an internal-knowledge question. Retrieved {len(hits)} candidate passage(s); "
                f"the evidence check accepted the best match (score {best_score:.2f})."
            )
        else:
            answer = "I cannot confirm this based on the available context. Add a relevant source document or configure web search, then try again."
            reasoning_summary = "Local retrieval and one reformulated pass did not find sufficiently relevant evidence; web fallback was attempted."

        # Keep the trace's retrieval summary useful to the UI without exposing internal prompts.
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        trace.append(self._trace_step("Response grounding", reasoning_summary, duration_ms=elapsed_ms))
        xml = self._build_xml(reasoning_summary, sources, answer)
        return {
            "query": clean_query,
            "route": route,
            "classification": {
                "primary": route,
                "needs_freshness": needs_freshness,
                "calculation_detected": is_calculation,
            },
            "answer": answer,
            "answer_xml": xml,
            "sources": sources,
            "trace": trace,
            "tool_calls": tool_calls,
            "retrieval": {
                "passes": retrieval_passes,
                "relevant": relevant,
                "candidate_count": len(hits),
                "document_count": self.store.document_count,
                "chunk_count": self.store.chunk_count,
            },
            "web_search_configured": self.web_search.configured,
            "elapsed_ms": elapsed_ms,
        }

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "mode": "local deterministic RAG",
            "documents": self.store.document_count,
            "chunks": self.store.chunk_count,
            "web_search_configured": self.web_search.configured,
            "tools": [tool["name"] for tool in self.tools.definitions()],
        }


__all__ = [
    "AgentEngine",
    "Document",
    "HashingEmbedder",
    "TavilySearch",
    "ToolRegistry",
    "VectorStore",
]
