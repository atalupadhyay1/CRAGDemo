# CRAG Studio

A dependency-free, runnable demo of an agentic RAG workflow. It pairs a local hybrid vector retriever with an evidence-quality check, one query-reformulation pass, structured tools, and an optional web-search fallback. Responses are returned in the requested `<reasoning>`, `<sources>`, and `<answer>` XML envelope; when the available evidence is not enough, the engine says so rather than guessing.

## Run locally

Requires Python 3.10+ and no third-party packages.

```bash
python server.py
```

Then open <http://localhost:8000>. To use another port, set `PORT=9000` or pass `--port 9000`. The server binds to `0.0.0.0` by default for local previews; do not expose this unauthenticated demo to an untrusted network.

## What is included

- **Local retrieval:** deterministic feature-hashed TF-IDF-style vectors, cosine similarity, and lexical overlap over stable, cited document chunks. No embedding download or hosted LLM is needed.
- **Agent loop:** query classification → vector retrieval → evidence check → query reformulation when needed → optional web fallback → grounded XML response.
- **Structured tools:** JSON-schema-described and validated calculator and web-search tools. Arithmetic uses a restricted AST evaluator rather than `eval`.
- **Optional live search:** configure `TAVILY_API_KEY` in the server environment to enable Tavily. Without it, fresh/current questions are explicitly left unconfirmed. Search queries are sent to Tavily when the fallback is used.
- **Knowledge base UI:** inspect the seeded sources and upload `.txt` or `.md` files. User uploads are indexed locally and persisted to `data/user_documents.json`; that runtime file is git-ignored.
- **Inspectable trace:** view routing, retrieval scores, reformulation, tool calls, and the exact XML response.

The included corpus is a small set of RAG/CRAG notes intended for exercising the demo, not a general-purpose knowledge base.

## Learning material

- [Agentic AI master course](AgenticAI/README.md) — progressive lessons from foundations through production multi-agent systems, with runnable labs.
- [1Z0-1157-26 practice test](practice_tests/1Z0-1157-26-practice-test.md) — original questions and a separate [answer key](practice_tests/1Z0-1157-26-answer-key.md).
- [Forward Deployed Engineer practice test](practice_tests/forward-deployed-engineer-practice-test.md) — role-readiness questions with a separate [answer key](practice_tests/forward-deployed-engineer-answer-key.md).

## Test

```bash
python -m unittest discover -s tests -v
```

## HTTP API

- `GET /api/health` — engine and provider status
- `GET /api/documents` — indexed document list
- `GET /api/tools` — registered tool definitions and JSON schemas
- `POST /api/query` — `{"query":"How does vector retrieval work?"}`
- `POST /api/documents` — `{"title":"Notes","content":"... at least 20 characters ..."}`
- `DELETE /api/documents/USER-<id>` — remove an uploaded source

`POST /api/query` returns `answer`, `answer_xml`, `sources`, `trace`, `tool_calls`, and retrieval metadata. The browser uses relative API paths, so it works behind a proxied preview origin.
