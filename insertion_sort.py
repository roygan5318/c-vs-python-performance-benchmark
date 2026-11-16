#!/usr/bin/env python3

import sys
import time
from pathlib import Path


def insertion_sort(values: list[int]) -> None:
    for i in range(1, len(values)):
        key = values[i]
        j = i

        while j > 0 and values[j - 1] > key:
            values[j] = values[j - 1]
            j -= 1
        values[j] = key


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} DATA_FILE")

    values = [int(value) for value in Path(sys.argv[1]).read_text().split()]

    start = time.perf_counter()
    insertion_sort(values)
    elapsed = time.perf_counter() - start

    if any(left > right for left, right in zip(values, values[1:])):
        raise RuntimeError("Sort verification failed")

    print(f"{elapsed:.9f} {sum(values)}")


if __name__ == "__main__":
    main()
