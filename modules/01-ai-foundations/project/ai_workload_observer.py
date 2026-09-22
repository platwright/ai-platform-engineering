#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PROMPT_FILE = SCRIPT_DIR / "prompts" / "foundation-check.txt"
DEFAULT_MOCK_FILE = SCRIPT_DIR / "fixtures" / "mock-success.json"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Capture latency, token usage, response text, and error data from a "
            "mock or OpenAI-compatible chat completions endpoint."
        )
    )
    parser.add_argument("--mode", choices=["mock", "http"], default="mock")
    parser.add_argument("--prompt-file", default=str(DEFAULT_PROMPT_FILE))
    parser.add_argument("--mock-file", default=str(DEFAULT_MOCK_FILE))
    parser.add_argument("--mock-latency-ms", type=float, default=120.0)
    parser.add_argument("--api-url", default=os.getenv("MODEL_API_URL", ""))
    parser.add_argument("--api-key", default=os.getenv("MODEL_API_KEY", ""))
    parser.add_argument("--model", default=os.getenv("MODEL_NAME", "example-foundation-model"))
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=200)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-file", default="")
    return parser.parse_args()


def load_text(path_text: str) -> str:
    path = Path(path_text)
    return path.read_text(encoding="utf-8").strip()


def load_json(path_text: str) -> Any:
    path = Path(path_text)
    return json.loads(path.read_text(encoding="utf-8"))


def truncate(value: str, limit: int = 160) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def build_payload(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "model": args.model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You explain AI concepts clearly for platform engineers and stay concise."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }


def parse_json_text(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": {"message": text, "type": "non_json_response", "code": None}}


def perform_mock_request(args: argparse.Namespace) -> tuple[int, dict[str, Any], dict[str, str], float]:
    fixture = load_json(args.mock_file)
    start = time.perf_counter()
    if args.mock_latency_ms > 0:
        time.sleep(args.mock_latency_ms / 1000.0)
    latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
    status_code = int(fixture.get("status_code", 200))
    body = fixture.get("body", {})
    headers = fixture.get("headers", {})
    return status_code, body, headers, latency_ms


def perform_http_request(
    args: argparse.Namespace, payload: dict[str, Any]
) -> tuple[int, dict[str, Any], dict[str, str], float]:
    if not args.api_url:
        raise ValueError("MODEL_API_URL or --api-url is required when --mode http is used.")
    if not args.api_key:
        raise ValueError("MODEL_API_KEY or --api-key is required when --mode http is used.")

    raw_payload = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=args.api_url,
        data=raw_payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {args.api_key}",
            "Content-Type": "application/json",
        },
    )

    start = time.perf_counter()
    try:
        with request.urlopen(req, timeout=args.timeout) as response:
            body_text = response.read().decode("utf-8", errors="replace")
            body = parse_json_text(body_text)
            headers = dict(response.headers.items())
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return response.status, body, headers, latency_ms
    except error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        body = parse_json_text(body_text)
        headers = dict(exc.headers.items()) if exc.headers else {}
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return exc.code, body, headers, latency_ms
    except error.URLError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return 0, {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}}, {}, latency_ms


def extract_usage(body: dict[str, Any]) -> dict[str, Any]:
    usage = body.get("usage", {}) if isinstance(body, dict) else {}
    return {
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }


def extract_response_text(body: dict[str, Any]) -> str | None:
    if not isinstance(body, dict):
        return None
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message", {})
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("text"):
                parts.append(str(item["text"]))
        return "\n".join(parts) if parts else None
    return None


def extract_finish_reason(body: dict[str, Any]) -> str | None:
    if not isinstance(body, dict):
        return None
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    finish_reason = first.get("finish_reason")
    return str(finish_reason) if finish_reason is not None else None


def extract_error(body: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(body, dict) or "error" not in body:
        return None
    raw_error = body.get("error")
    if isinstance(raw_error, dict):
        return {
            "message": raw_error.get("message"),
            "type": raw_error.get("type"),
            "code": raw_error.get("code"),
        }
    return {"message": str(raw_error), "type": None, "code": None}


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_report(
    args: argparse.Namespace,
    prompt: str,
    status_code: int,
    body: dict[str, Any],
    headers: dict[str, str],
    latency_ms: float,
) -> dict[str, Any]:
    return {
        "timestamp_utc": iso_timestamp(),
        "mode": args.mode,
        "success": 200 <= status_code < 300 and extract_error(body) is None,
        "request": {
            "api_url": args.api_url if args.mode == "http" else None,
            "model": args.model,
            "prompt_file": str(Path(args.prompt_file)),
            "prompt_preview": truncate(prompt),
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "timeout_seconds": args.timeout,
        },
        "response": {
            "status_code": status_code,
            "request_id": headers.get("x-request-id") or headers.get("x-request-id".title()),
            "model": body.get("model") if isinstance(body, dict) else None,
            "latency_ms": latency_ms,
            "usage": extract_usage(body),
            "finish_reason": extract_finish_reason(body),
            "text": extract_response_text(body),
            "error": extract_error(body),
        },
        "raw_response": body,
    }


def write_report(report: dict[str, Any], args: argparse.Namespace) -> Path:
    if args.output_file:
        destination = Path(args.output_file)
        destination.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
        destination = output_dir / filename
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


def print_summary(report: dict[str, Any], output_path: Path) -> None:
    response = report["response"]
    usage = response["usage"]
    print(f"Report written to: {output_path}")
    print(f"Status code: {response['status_code']}")
    print(f"Latency (ms): {response['latency_ms']}")
    print(
        "Usage tokens: prompt={prompt} completion={completion} total={total}".format(
            prompt=usage.get("prompt_tokens"),
            completion=usage.get("completion_tokens"),
            total=usage.get("total_tokens"),
        )
    )
    if response.get("finish_reason"):
        print(f"Finish reason: {response['finish_reason']}")
    if response.get("text"):
        print(f"Response preview: {truncate(response['text'], 120)}")
    if response.get("error"):
        print(f"Error: {response['error']['message']}", file=sys.stderr)


def main() -> int:
    args = parse_args()
    prompt = load_text(args.prompt_file)
    payload = build_payload(prompt, args)

    try:
        if args.mode == "mock":
            status_code, body, headers, latency_ms = perform_mock_request(args)
        else:
            status_code, body, headers, latency_ms = perform_http_request(args, payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Request setup failed: {exc}", file=sys.stderr)
        return 2

    report = build_report(args, prompt, status_code, body, headers, latency_ms)
    output_path = write_report(report, args)
    print_summary(report, output_path)
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())