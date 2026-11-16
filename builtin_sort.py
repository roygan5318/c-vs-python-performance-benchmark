#!/usr/bin/env python3

"""Exploratory benchmark using Python's native built-in sorting function.

This is intentionally separate from the fair insertion-sort comparison:
``sorted`` is implemented in CPython's native runtime and uses Timsort, not
insertion sort.  It demonstrates why moving a whole operation into an
optimized library can avoid the cost of a Python-level loop.
"""

import sys
import time
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} DATA_FILE")

    values = [int(value) for value in Path(sys.argv[1]).read_text().split()]

    start = time.perf_counter()
    values = sorted(values)
    elapsed = time.perf_counter() - start

    if any(left > right for left, right in zip(values, values[1:])):
        raise RuntimeError("Sort verification failed")

    print(f"{elapsed:.9f} {sum(values)}")


if __name__ == "__main__":
    main()
