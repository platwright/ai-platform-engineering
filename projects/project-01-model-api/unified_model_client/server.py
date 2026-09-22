from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from .service import UnifiedModelClient


def normalize_status(status_code: int) -> int:
    if 400 <= status_code <= 599:
        return status_code
    return 502


def create_http_server(client: UnifiedModelClient, host: str, port: int) -> ThreadingHTTPServer:
    class RequestHandler(BaseHTTPRequestHandler):
        def write_json(self, status_code: int, payload: dict[str, Any]) -> None:
            raw = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/healthz":
                self.write_json(
                    200,
                    {
                        "status": "ok",
                        "application": client.config.app_name,
                        "environment": client.config.environment,
                    },
                )
                return
            if parsed.path == "/providers":
                self.write_json(200, {"providers": client.list_providers()})
                return
            self.write_json(404, {"error": {"message": "Not found"}})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != "/api/chat":
                self.write_json(404, {"error": {"message": "Not found"}})
                return

            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                content_length = 0

            if content_length <= 0:
                self.write_json(400, {"error": {"message": "Request body is required"}})
                return

            try:
                payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            except json.JSONDecodeError:
                self.write_json(400, {"error": {"message": "Request body must be valid JSON"}})
                return

            message = payload.get("message")
            if not isinstance(message, str) or not message.strip():
                self.write_json(400, {"error": {"message": "Field 'message' must be a non-empty string"}})
                return

            overrides: dict[str, Any] = {}
            if "temperature" in payload:
                overrides["temperature"] = payload["temperature"]
            if "max_tokens" in payload:
                overrides["max_tokens"] = payload["max_tokens"]
            if "timeout_seconds" in payload:
                overrides["timeout_seconds"] = payload["timeout_seconds"]

            try:
                report = client.chat(
                    provider_alias=payload.get("provider"),
                    message=message,
                    overrides=overrides,
                )
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                self.write_json(400, {"error": {"message": str(exc)}})
                return

            status_code = 200 if report["success"] else normalize_status(report["response"]["status_code"])
            self.write_json(status_code, report)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return ThreadingHTTPServer((host, port), RequestHandler)