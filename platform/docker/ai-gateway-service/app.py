#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from collections import deque
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import urljoin, urlparse

APP_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = APP_DIR / "config" / "app.example.json"
DEFAULT_SAVE_DIR = APP_DIR / "runs"
WHITESPACE = re.compile(r"\s+")


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: str) -> str:
    return WHITESPACE.sub(" ", value.strip().lower())


def truncate(value: str, limit: int = 180) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Local AI gateway service for routing, fallback, rate limiting, and usage tracking."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))

    subparsers = parser.add_subparsers(dest="command", required=True)

    route_parser = subparsers.add_parser("route", help="Show the routing decision for one message")
    route_parser.add_argument("--message", required=True)
    route_parser.set_defaults(handler=handle_route)

    request_parser = subparsers.add_parser("request", help="Send one request through the gateway")
    request_parser.add_argument("--message", required=True)
    request_parser.add_argument("--application-id", default="sample-chat")
    request_parser.add_argument("--provider-override", default="")
    request_parser.add_argument("--temperature", type=float)
    request_parser.add_argument("--max-tokens", type=int)
    request_parser.add_argument("--timeout", type=float)
    request_parser.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    request_parser.add_argument("--no-save", action="store_true")
    request_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    request_parser.set_defaults(handler=handle_request)

    serve_parser = subparsers.add_parser("serve", help="Run the gateway HTTP API")
    serve_parser.add_argument("--host", default="")
    serve_parser.add_argument("--port", type=int)
    serve_parser.set_defaults(handler=handle_serve)

    return parser.parse_args()


def resolve_path(base_dir: Path, raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def load_config(config_path: str) -> dict[str, Any]:
    path = Path(config_path).resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    application = raw.get("application", {})
    backend = raw.get("backend_model_api", {})
    routing = raw.get("routing", {})
    policies = raw.get("policies", {})
    return {
        "config_path": path,
        "application": {
            "name": application.get("name", "local-ai-gateway"),
            "environment": application.get("environment", "local"),
            "listen_host": application.get("listen_host", "127.0.0.1"),
            "listen_port": int(application.get("listen_port", 8090)),
        },
        "backend_model_api": {
            "base_url": os.getenv("PROJECT01_API_BASE_URL", backend.get("base_url", "http://127.0.0.1:8000")),
            "timeout_seconds": float(backend.get("timeout_seconds", 30)),
        },
        "routing": {
            "default_provider": routing.get("default_provider", "acme-reliable"),
            "simple_request_max_chars": int(routing.get("simple_request_max_chars", 120)),
            "simple_request_provider": routing.get("simple_request_provider", "acme-fast"),
            "sensitive_terms": [str(term).lower() for term in routing.get("sensitive_terms", [])],
            "sensitive_provider": routing.get("sensitive_provider", "acme-reliable"),
            "fallback_provider": routing.get("fallback_provider", "acme-reliable"),
        },
        "policies": {
            "rate_limit_per_minute": int(policies.get("rate_limit_per_minute", 10)),
            "exact_prompt_cache_enabled": bool(policies.get("exact_prompt_cache_enabled", True)),
            "cache_ttl_seconds": int(policies.get("cache_ttl_seconds", 300)),
        },
    }


class GatewayState:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.request_times: dict[str, deque[float]] = {}
        self.cache: dict[str, dict[str, Any]] = {}
        self.metrics = {
            "requests_total": 0,
            "cache_hits": 0,
            "fallbacks": 0,
            "rate_limited": 0,
            "providers": {},
        }

    def _trim(self, queue: deque[float], window_seconds: float, now: float) -> None:
        while queue and now - queue[0] > window_seconds:
            queue.popleft()

    def check_and_record_rate_limit(self, application_id: str, limit: int) -> tuple[bool, int]:
        now = time.time()
        with self.lock:
            queue = self.request_times.setdefault(application_id, deque())
            self._trim(queue, 60.0, now)
            if len(queue) >= limit:
                self.metrics["rate_limited"] += 1
                return False, len(queue)
            queue.append(now)
            return True, len(queue)

    def get_cache(self, key: str, ttl_seconds: int) -> dict[str, Any] | None:
        now = time.time()
        with self.lock:
            item = self.cache.get(key)
            if item is None:
                return None
            if now - float(item["created_at_epoch"]) > ttl_seconds:
                self.cache.pop(key, None)
                return None
            self.metrics["cache_hits"] += 1
            return item["report"]

    def set_cache(self, key: str, report: dict[str, Any]) -> None:
        with self.lock:
            self.cache[key] = {"created_at_epoch": time.time(), "report": report}

    def record_provider(self, provider: str, success: bool, fallback_used: bool) -> None:
        with self.lock:
            self.metrics["requests_total"] += 1
            if fallback_used:
                self.metrics["fallbacks"] += 1
            provider_metrics = self.metrics["providers"].setdefault(provider, {"requests": 0, "successes": 0, "failures": 0})
            provider_metrics["requests"] += 1
            if success:
                provider_metrics["successes"] += 1
            else:
                provider_metrics["failures"] += 1

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return json.loads(json.dumps(self.metrics))


def route_request(message: str, config: dict[str, Any], provider_override: str | None = None) -> tuple[str, str]:
    if provider_override:
        return provider_override, "provider override"
    normalized = normalize_text(message)
    sensitive_terms = config["routing"]["sensitive_terms"]
    if any(term in normalized for term in sensitive_terms):
        return config["routing"]["sensitive_provider"], "sensitive content routing"
    if len(message) <= config["routing"]["simple_request_max_chars"]:
        return config["routing"]["simple_request_provider"], "short request routing"
    return config["routing"]["default_provider"], "default routing"


def call_project01(
    config: dict[str, Any],
    provider: str,
    message: str,
    application_id: str,
    overrides: dict[str, Any],
) -> tuple[int, dict[str, Any], float]:
    url = urljoin(config["backend_model_api"]["base_url"].rstrip("/") + "/", "api/chat")
    payload = {"provider": provider, "message": message, "application_id": application_id}
    payload.update(overrides)
    req = request.Request(
        url=url,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    timeout_seconds = float(overrides.get("timeout_seconds", config["backend_model_api"]["timeout_seconds"]))
    start = time.perf_counter()
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8", errors="replace"))
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return response.status, body, latency_ms
    except error.HTTPError as exc:
        body = json.loads(exc.read().decode("utf-8", errors="replace"))
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return exc.code, body, latency_ms
    except error.URLError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return 0, {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}}, latency_ms


def build_report(
    config: dict[str, Any],
    application_id: str,
    original_message: str,
    routed_provider: str,
    routing_reason: str,
    response_status: int,
    response_body: dict[str, Any],
    gateway_latency_ms: float,
    backend_latency_ms: float,
    fallback_provider: str | None,
    cache_hit: bool,
) -> dict[str, Any]:
    backend_response = response_body.get("response", {}) if isinstance(response_body, dict) and "response" in response_body else response_body
    backend_error = backend_response.get("error") if isinstance(backend_response, dict) else None
    success = 200 <= response_status < 300 and backend_error is None
    return {
        "timestamp_utc": iso_timestamp(),
        "gateway": {
            "name": config["application"]["name"],
            "environment": config["application"]["environment"],
            "routing_reason": routing_reason,
            "cache_hit": cache_hit,
            "fallback_provider": fallback_provider,
        },
        "request": {
            "application_id": application_id,
            "message_preview": truncate(original_message),
            "selected_provider": routed_provider,
        },
        "success": success,
        "response": {
            "status_code": response_status,
            "gateway_latency_ms": gateway_latency_ms,
            "backend_latency_ms": backend_latency_ms,
            "text": backend_response.get("text") if isinstance(backend_response, dict) else None,
            "usage": backend_response.get("usage") if isinstance(backend_response, dict) else None,
            "model": backend_response.get("model") if isinstance(backend_response, dict) else None,
            "error": backend_error or response_body.get("error"),
        },
        "backend_report": response_body,
    }


def execute_gateway_request(
    config: dict[str, Any],
    state: GatewayState,
    message: str,
    application_id: str,
    provider_override: str | None,
    overrides: dict[str, Any],
) -> dict[str, Any]:
    allowed, current_count = state.check_and_record_rate_limit(
        application_id, int(config["policies"]["rate_limit_per_minute"])
    )
    if not allowed:
        return {
            "timestamp_utc": iso_timestamp(),
            "gateway": {
                "name": config["application"]["name"],
                "environment": config["application"]["environment"],
                "routing_reason": "rate limited",
                "cache_hit": False,
                "fallback_provider": None,
            },
            "request": {
                "application_id": application_id,
                "message_preview": truncate(message),
                "selected_provider": None,
            },
            "success": False,
            "response": {
                "status_code": 429,
                "gateway_latency_ms": 0.0,
                "backend_latency_ms": 0.0,
                "text": None,
                "usage": None,
                "model": None,
                "error": {
                    "message": f"Rate limit exceeded for application_id={application_id} with {current_count} requests in the last minute.",
                    "type": "rate_limit_error",
                    "code": "gateway_rate_limit_exceeded",
                },
            },
            "backend_report": None,
        }

    cache_key = f"{application_id}:{normalize_text(message)}"
    if config["policies"]["exact_prompt_cache_enabled"]:
        cached = state.get_cache(cache_key, int(config["policies"]["cache_ttl_seconds"]))
        if cached is not None:
            cached_report = json.loads(json.dumps(cached))
            cached_report["timestamp_utc"] = iso_timestamp()
            cached_report["gateway"]["cache_hit"] = True
            state.record_provider(
                cached_report["request"].get("selected_provider") or "cached",
                bool(cached_report["success"]),
                False,
            )
            return cached_report

    provider, routing_reason = route_request(message, config, provider_override)
    gateway_start = time.perf_counter()
    status_code, body, backend_latency_ms = call_project01(config, provider, message, application_id, overrides)
    fallback_provider = None

    backend_response = body.get("response", {}) if isinstance(body, dict) and "response" in body else body
    backend_error = backend_response.get("error") if isinstance(backend_response, dict) else None
    success = 200 <= status_code < 300 and backend_error is None

    if not success:
        configured_fallback = config["routing"]["fallback_provider"]
        if configured_fallback and configured_fallback != provider:
            fallback_provider = configured_fallback
            fallback_status, fallback_body, fallback_latency_ms = call_project01(
                config, configured_fallback, message, application_id, overrides
            )
            fallback_backend_response = fallback_body.get("response", {}) if isinstance(fallback_body, dict) and "response" in fallback_body else fallback_body
            fallback_error = fallback_backend_response.get("error") if isinstance(fallback_backend_response, dict) else None
            fallback_success = 200 <= fallback_status < 300 and fallback_error is None
            if fallback_success:
                provider = configured_fallback
                routing_reason = routing_reason + " + fallback"
                status_code = fallback_status
                body = fallback_body
                backend_latency_ms = fallback_latency_ms
                success = True

    gateway_latency_ms = round((time.perf_counter() - gateway_start) * 1000.0, 2)
    report = build_report(
        config=config,
        application_id=application_id,
        original_message=message,
        routed_provider=provider,
        routing_reason=routing_reason,
        response_status=status_code,
        response_body=body,
        gateway_latency_ms=gateway_latency_ms,
        backend_latency_ms=backend_latency_ms,
        fallback_provider=fallback_provider,
        cache_hit=False,
    )
    state.record_provider(provider, bool(report["success"]), fallback_provider is not None and bool(report["success"]))
    if report["success"] and config["policies"]["exact_prompt_cache_enabled"]:
        state.set_cache(cache_key, report)
    return report


def save_report(report: dict[str, Any], save_dir: str) -> Path:
    destination_dir = Path(save_dir).resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = f"gateway-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
    destination = destination_dir / filename
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


def print_summary(report: dict[str, Any], output_path: Path | None) -> None:
    response = report["response"]
    print(f"Application ID: {report['request']['application_id']}")
    print(f"Selected provider: {report['request']['selected_provider']}")
    print(f"Status code: {response['status_code']}")
    print(f"Gateway latency (ms): {response['gateway_latency_ms']}")
    print(f"Backend latency (ms): {response['backend_latency_ms']}")
    if response.get("text"):
        print(f"Response preview: {truncate(response['text'])}")
    if response.get("error"):
        print(f"Error: {response['error']['message']}", file=sys.stderr)
    if output_path is not None:
        print(f"Run artifact: {output_path}")


def build_overrides(args: argparse.Namespace) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    if getattr(args, "temperature", None) is not None:
        overrides["temperature"] = args.temperature
    if getattr(args, "max_tokens", None) is not None:
        overrides["max_tokens"] = args.max_tokens
    if getattr(args, "timeout", None) is not None:
        overrides["timeout_seconds"] = args.timeout
    return overrides


def handle_route(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    provider, reason = route_request(args.message, config)
    print(f"Provider: {provider}")
    print(f"Reason: {reason}")
    return 0


def handle_request(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state = GatewayState()
    try:
        report = execute_gateway_request(
            config=config,
            state=state,
            message=args.message,
            application_id=args.application_id,
            provider_override=args.provider_override or None,
            overrides=build_overrides(args),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Gateway request failed before execution: {exc}", file=sys.stderr)
        return 2

    output_path: Path | None = None
    if not args.no_save:
        output_path = save_report(report, args.save_dir)
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_summary(report, output_path)
    return 0 if report["success"] else 1


def create_http_server(config: dict[str, Any], state: GatewayState, host: str, port: int) -> ThreadingHTTPServer:
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
                        "application": config["application"]["name"],
                        "environment": config["application"]["environment"],
                    },
                )
                return
            if parsed.path == "/metrics":
                self.write_json(200, state.snapshot())
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
                report = execute_gateway_request(
                    config=config,
                    state=state,
                    message=message,
                    application_id=str(payload.get("application_id") or "unknown-app"),
                    provider_override=str(payload.get("provider_override") or "") or None,
                    overrides=overrides,
                )
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                self.write_json(400, {"error": {"message": str(exc)}})
                return
            status_code = 200 if report["success"] else int(report["response"]["status_code"] or 502)
            self.write_json(status_code, report)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return ThreadingHTTPServer((host, port), RequestHandler)


def handle_serve(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state = GatewayState()
    host = args.host or config["application"]["listen_host"]
    port = args.port or config["application"]["listen_port"]
    server = create_http_server(config, state, host, port)
    print(f"Serving AI gateway on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down AI gateway.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())