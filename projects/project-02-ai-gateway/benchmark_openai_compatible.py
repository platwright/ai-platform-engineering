#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_PROMPTS = PROJECT_DIR / "prompts" / "benchmark-prompts.txt"
DEFAULT_MOCK_SERIES = PROJECT_DIR / "fixtures" / "benchmark-mock-series.json"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "runs"


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark an OpenAI-compatible chat completions endpoint and write a basic performance report."
    )
    parser.add_argument("--mode", choices=["mock", "http"], default="mock")
    parser.add_argument("--endpoint", default=os.getenv("OPENAI_COMPATIBLE_API_URL", ""))
    parser.add_argument("--api-key", default=os.getenv("OPENAI_COMPATIBLE_API_KEY", ""))
    parser.add_argument("--model", default=os.getenv("OPENAI_COMPATIBLE_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0"))
    parser.add_argument("--prompts-file", default=str(DEFAULT_PROMPTS))
    parser.add_argument("--mock-series-file", default=str(DEFAULT_MOCK_SERIES))
    parser.add_argument("--requests", type=int, default=8)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser.parse_args()


def load_prompts(path_text: str) -> list[str]:
    lines = Path(path_text).read_text(encoding="utf-8").splitlines()
    prompts = [line.strip() for line in lines if line.strip()]
    if not prompts:
        raise ValueError("At least one prompt is required.")
    return prompts


def load_mock_series(path_text: str) -> list[dict[str, Any]]:
    raw = json.loads(Path(path_text).read_text(encoding="utf-8"))
    responses = raw.get("responses", [])
    if not isinstance(responses, list) or not responses:
        raise ValueError("Mock series file must contain a non-empty 'responses' array.")
    return responses


def percentile(values: list[float], target: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return round(ordered[0], 2)
    rank = target * (len(ordered) - 1)
    lower = int(rank)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = rank - lower
    interpolated = ordered[lower] + (ordered[upper] - ordered[lower]) * fraction
    return round(interpolated, 2)


def build_payload(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "model": args.model,
        "messages": [
            {
                "role": "system",
                "content": "You explain AI inference behavior concisely for platform engineers.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }


def parse_json_text(raw_text: str) -> Any:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"error": {"message": raw_text, "type": "non_json_response", "code": None}}


def extract_usage(body: dict[str, Any]) -> dict[str, Any]:
    usage = body.get("usage", {}) if isinstance(body, dict) else {}
    return {
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }


def extract_text(body: dict[str, Any]) -> str | None:
    choices = body.get("choices") if isinstance(body, dict) else None
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


def extract_error(body: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(body, dict) or "error" not in body:
        return None
    raw_error = body["error"]
    if isinstance(raw_error, dict):
        return {
            "message": raw_error.get("message"),
            "type": raw_error.get("type"),
            "code": raw_error.get("code"),
        }
    return {"message": str(raw_error), "type": None, "code": None}


def run_mock_request(series: list[dict[str, Any]], index: int) -> tuple[int, dict[str, Any], float]:
    item = series[index % len(series)]
    latency_ms = float(item.get("latency_ms", 100.0))
    time.sleep(latency_ms / 1000.0)
    return int(item.get("status_code", 200)), item.get("body", {}), latency_ms


def run_http_request(args: argparse.Namespace, payload: dict[str, Any]) -> tuple[int, dict[str, Any], float]:
    if not args.endpoint:
        raise ValueError("--endpoint or OPENAI_COMPATIBLE_API_URL is required in http mode.")
    headers = {"Content-Type": "application/json"}
    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"
    req = request.Request(
        url=args.endpoint,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
    )
    start = time.perf_counter()
    try:
        with request.urlopen(req, timeout=args.timeout) as response:
            body_text = response.read().decode("utf-8", errors="replace")
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return response.status, parse_json_text(body_text), latency_ms
    except error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return exc.code, parse_json_text(body_text), latency_ms
    except error.URLError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return 0, {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}}, latency_ms


def execute_one(index: int, prompt: str, args: argparse.Namespace, series: list[dict[str, Any]] | None) -> dict[str, Any]:
    payload = build_payload(prompt, args)
    if args.mode == "mock":
        assert series is not None
        status_code, body, latency_ms = run_mock_request(series, index)
    else:
        status_code, body, latency_ms = run_http_request(args, payload)
    usage = extract_usage(body)
    completion_tokens = usage.get("completion_tokens")
    tokens_per_second = None
    if completion_tokens is not None and latency_ms > 0:
        tokens_per_second = round(float(completion_tokens) / (latency_ms / 1000.0), 2)
    error_object = extract_error(body)
    return {
        "index": index,
        "success": 200 <= status_code < 300 and error_object is None,
        "status_code": status_code,
        "latency_ms": latency_ms,
        "prompt": prompt,
        "model": body.get("model") if isinstance(body, dict) else None,
        "usage": usage,
        "completion_tokens_per_second": tokens_per_second,
        "text_preview": extract_text(body),
        "error": error_object,
    }


def build_summary(args: argparse.Namespace, started_at: float, completed_at: float, results: list[dict[str, Any]]) -> dict[str, Any]:
    successes = [item for item in results if item["success"]]
    failures = [item for item in results if not item["success"]]
    latencies = [float(item["latency_ms"]) for item in results]
    tokens_per_second = [float(item["completion_tokens_per_second"]) for item in results if item["completion_tokens_per_second"] is not None]
    total_completion_tokens = sum(
        int(item["usage"]["completion_tokens"])
        for item in results
        if item["usage"].get("completion_tokens") is not None
    )
    wall_time_ms = round((completed_at - started_at) * 1000.0, 2)
    overall_tokens_per_second = None
    if total_completion_tokens > 0 and wall_time_ms > 0:
        overall_tokens_per_second = round(total_completion_tokens / (wall_time_ms / 1000.0), 2)

    return {
        "mode": args.mode,
        "endpoint": args.endpoint if args.mode == "http" else None,
        "model": args.model,
        "requests": args.requests,
        "concurrency": args.concurrency,
        "successful_requests": len(successes),
        "failed_requests": len(failures),
        "success_rate": round(len(successes) / len(results), 4) if results else 0.0,
        "wall_time_ms": wall_time_ms,
        "latency_ms": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
            "max": round(max(latencies), 2) if latencies else None,
        },
        "completion_tokens_per_second": {
            "p50": percentile(tokens_per_second, 0.50),
            "p95": percentile(tokens_per_second, 0.95),
            "max": round(max(tokens_per_second), 2) if tokens_per_second else None,
            "overall": overall_tokens_per_second,
        },
    }


def write_reports(output_dir_text: str, report: dict[str, Any]) -> tuple[Path, Path]:
    output_dir = Path(output_dir_text).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    json_path = output_dir / f"benchmark-{stamp}.json"
    md_path = output_dir / f"benchmark-{stamp}.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = report["summary"]
    md_lines = [
        "# Benchmark Report",
        "",
        f"- Timestamp: {report['timestamp_utc']}",
        f"- Mode: {summary['mode']}",
        f"- Model: {summary['model']}",
        f"- Requests: {summary['requests']}",
        f"- Concurrency: {summary['concurrency']}",
        f"- Success rate: {summary['success_rate']}",
        f"- Wall time (ms): {summary['wall_time_ms']}",
        "",
        "## Latency",
        "",
        f"- p50: {summary['latency_ms']['p50']}",
        f"- p95: {summary['latency_ms']['p95']}",
        f"- p99: {summary['latency_ms']['p99']}",
        f"- max: {summary['latency_ms']['max']}",
        "",
        "## Completion Tokens Per Second",
        "",
        f"- p50: {summary['completion_tokens_per_second']['p50']}",
        f"- p95: {summary['completion_tokens_per_second']['p95']}",
        f"- max: {summary['completion_tokens_per_second']['max']}",
        f"- overall: {summary['completion_tokens_per_second']['overall']}",
        "",
        "## Failures",
        "",
        f"- Failed requests: {summary['failed_requests']}",
    ]
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return json_path, md_path


def print_summary(summary: dict[str, Any], json_path: Path, md_path: Path) -> None:
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    print(f"Requests: {summary['requests']}")
    print(f"Success rate: {summary['success_rate']}")
    print(
        "Latency ms: p50={p50} p95={p95} p99={p99} max={max}".format(
            p50=summary["latency_ms"]["p50"],
            p95=summary["latency_ms"]["p95"],
            p99=summary["latency_ms"]["p99"],
            max=summary["latency_ms"]["max"],
        )
    )
    print(
        "Completion tokens/sec: p50={p50} p95={p95} overall={overall}".format(
            p50=summary["completion_tokens_per_second"]["p50"],
            p95=summary["completion_tokens_per_second"]["p95"],
            overall=summary["completion_tokens_per_second"]["overall"],
        )
    )


def main() -> int:
    args = parse_args()
    prompts = load_prompts(args.prompts_file)
    series = load_mock_series(args.mock_series_file) if args.mode == "mock" else None
    started_at = time.perf_counter()
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        futures = []
        for index in range(args.requests):
            prompt = prompts[index % len(prompts)]
            futures.append(executor.submit(execute_one, index, prompt, args, series))
        for future in as_completed(futures):
            results.append(future.result())
    completed_at = time.perf_counter()
    ordered_results = sorted(results, key=lambda item: item["index"])
    summary = build_summary(args, started_at, completed_at, ordered_results)
    report = {
        "timestamp_utc": iso_timestamp(),
        "summary": summary,
        "results": ordered_results,
    }
    json_path, md_path = write_reports(args.output_dir, report)
    print_summary(summary, json_path, md_path)
    return 0 if summary["failed_requests"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())