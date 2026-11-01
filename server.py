"""Run the CRAG Demo without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from rag_engine import AgentEngine


ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
SAMPLE_DOCS = ROOT / "data" / "sample_docs.json"
USER_DOCS = ROOT / "data" / "user_documents.json"
ENGINE = AgentEngine.from_json_files(SAMPLE_DOCS, USER_DOCS)


class CRAGRequestHandler(BaseHTTPRequestHandler):
    server_version = "CRAGDemo/1.0"

    def log_message(self, format: str, *args: object) -> None:
        # Keep the local dev console readable; request bodies and API keys are never logged.
        super().log_message(format, *args)

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _read_json(self) -> dict[str, object]:
        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError as error:
            raise ValueError("Invalid request body length.") from error
        if length < 0 or length > 1_100_000:
            raise ValueError("Request body must be 1.1 MB or smaller.")
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("Request body must contain valid JSON.") from error
        if not isinstance(value, dict):
            raise ValueError("Request body must be a JSON object.")
        return value

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        path = unquote(urlsplit(self.path).path)
        if path == "/api/health":
            self._send_json(200, ENGINE.health())
            return
        if path == "/api/documents":
            self._send_json(200, {"documents": ENGINE.list_documents()})
            return
        if path == "/api/tools":
            self._send_json(200, {"tools": ENGINE.tools.definitions()})
            return
        if path.startswith("/api/"):
            self._send_json(404, {"error": "API route not found."})
            return

        if path in {"/", "/index.html"}:
            file_path = STATIC_DIR / "index.html"
        elif path.startswith("/static/"):
            relative = Path(path.removeprefix("/static/"))
            file_path = (STATIC_DIR / relative).resolve()
            if not file_path.is_relative_to(STATIC_DIR.resolve()):
                self._send_json(403, {"error": "Forbidden."})
                return
        else:
            self._send_json(404, {"error": "Not found."})
            return

        if not file_path.is_file():
            self._send_json(404, {"error": "File not found."})
            return
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "image/svg+xml"}:
            content_type += "; charset=utf-8"
        self._send_bytes(200, file_path.read_bytes(), content_type)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        path = urlsplit(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/query":
                query = payload.get("query")
                if not isinstance(query, str):
                    raise ValueError("The 'query' field must be a string.")
                self._send_json(200, ENGINE.query(query))
                return
            if path == "/api/documents":
                title = payload.get("title")
                content = payload.get("content")
                if not isinstance(title, str) or not isinstance(content, str):
                    raise ValueError("Both 'title' and 'content' must be strings.")
                document = ENGINE.add_document(title, content)
                self._send_json(201, {"document": document, "documents": ENGINE.list_documents()})
                return
            self._send_json(404, {"error": "API route not found."})
        except ValueError as error:
            self._send_json(400, {"error": str(error)})
        except (OSError, RuntimeError) as error:
            self._send_json(500, {"error": f"The request could not be completed: {error}"})

    def do_DELETE(self) -> None:  # noqa: N802 - stdlib handler API
        path = unquote(urlsplit(self.path).path)
        prefix = "/api/documents/"
        if not path.startswith(prefix):
            self._send_json(404, {"error": "API route not found."})
            return
        document_id = path[len(prefix):]
        if not document_id or "/" in document_id:
            self._send_json(400, {"error": "A valid document ID is required."})
            return
        if not ENGINE.delete_document(document_id):
            self._send_json(404, {"error": "Uploaded document not found."})
            return
        self._send_json(200, {"deleted": document_id, "documents": ENGINE.list_documents()})

    def do_HEAD(self) -> None:  # noqa: N802 - stdlib handler API
        path = urlsplit(self.path).path
        if path == "/":
            file_path = STATIC_DIR / "index.html"
            if file_path.is_file():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.end_headers()
                return
        self.send_error(404)


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the dependency-free CRAG Demo web app.")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"), help="Interface to bind (default: 0.0.0.0).")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), help="Port to listen on (default: 8000).")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), CRAGRequestHandler)
    server.daemon_threads = True
    print(f"CRAG Demo listening on http://{args.host}:{args.port}")
    print("Local vector retrieval is ready. Configure TAVILY_API_KEY to enable live web search.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down CRAG Demo.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
