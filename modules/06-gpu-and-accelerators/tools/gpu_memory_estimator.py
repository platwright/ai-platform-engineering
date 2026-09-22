#!/usr/bin/env python3

from __future__ import annotations

import argparse


PRECISION_BYTES = {
    "fp32": 4,
    "fp16": 2,
    "bf16": 2,
    "int8": 1,
    "int4": 0.5,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate model weight and KV cache memory for a serving workload."
    )
    parser.add_argument("--parameters-billions", type=float, required=True)
    parser.add_argument("--precision", choices=sorted(PRECISION_BYTES.keys()), required=True)
    parser.add_argument("--layers", type=int, required=True)
    parser.add_argument("--hidden-size", type=int, required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--context-tokens", type=int, required=True)
    parser.add_argument("--kv-bytes-per-element", type=float, default=2.0)
    parser.add_argument("--headroom-factor", type=float, default=1.2)
    return parser.parse_args()


def to_gib(value_in_bytes: float) -> float:
    return value_in_bytes / (1024 ** 3)


def main() -> int:
    args = parse_args()
    bytes_per_param = PRECISION_BYTES[args.precision]
    parameter_count = args.parameters_billions * 1_000_000_000

    weight_bytes = parameter_count * bytes_per_param
    kv_cache_bytes = (
        2
        * args.layers
        * args.hidden_size
        * args.batch_size
        * args.context_tokens
        * args.kv_bytes_per_element
    )
    total_bytes = weight_bytes + kv_cache_bytes
    recommended_bytes = total_bytes * args.headroom_factor

    print(f"Precision: {args.precision} ({bytes_per_param} bytes/parameter)")
    print(f"Weight memory estimate (GiB): {to_gib(weight_bytes):.2f}")
    print(f"KV cache estimate (GiB): {to_gib(kv_cache_bytes):.2f}")
    print(f"Combined minimum estimate (GiB): {to_gib(total_bytes):.2f}")
    print(f"Recommended with headroom (GiB): {to_gib(recommended_bytes):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())