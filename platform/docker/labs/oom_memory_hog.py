from __future__ import annotations

import time


def main() -> None:
    blocks: list[bytes] = []
    chunk_size = 10 * 1024 * 1024
    chunk_count = 0
    while True:
        blocks.append(b"x" * chunk_size)
        chunk_count += 1
        print(f"Allocated approximately {chunk_count * 10} MiB", flush=True)
        time.sleep(0.2)


if __name__ == "__main__":
    main()