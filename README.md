# Same Algorithm, Different Speed: C vs. Python

This project benchmarks equivalent insertion-sort implementations in C and Python. It asks:

> When C and Python implement the same O(n²) algorithm, how do their execution times compare as the input size increases?

## What the project controls

- Both programs implement the same insertion-sort algorithm.
- Both receive the exact same randomly generated arrays.
- Array creation, file reading, output, and process startup are excluded from the measured time.
- Every result is checked for correct sorted order and matching checksums.
- The runner alternates which language runs first and reports the median of repeated trials.
- The C program is compiled with `-O2`; this is disclosed because optimization affects performance.

## Requirements

- Python 3.9 or newer
- A C compiler available as `cc`, `clang`, or `gcc`

No third-party Python packages are required.

## Run the benchmark

```bash
python3 benchmark.py
```

The runner creates:

- `results.csv`: data suitable for a spreadsheet
- `RESULTS.md`: a formatted result table and interpretation
- `results.svg`: a graph comparing median execution times

You can change the experiment:

```bash
python3 benchmark.py --sizes 500 1000 2000 4000 --repetitions 15 --seed 211
```

## Timing methods

- C uses `clock_gettime(CLOCK_MONOTONIC, ...)`.
- Python uses `time.perf_counter()`.

These monotonic, high-resolution clocks are appropriate for measuring elapsed time.

## Why repeat measurements?

Execution time changes slightly because of operating-system scheduling, background programs, CPU frequency, caching, and other activity. Repeating the experiment and taking the median reduces the effect of unusually fast or slow measurements.

## Interpreting the results

Big-O describes how work grows with input size; it does not predict the exact number of seconds. Both versions are O(n²), but C is expected to have a smaller constant factor because it is compiled to native instructions. CPython executes bytecode and performs dynamic type and object handling during each operation.

The conclusion should be limited to this algorithm, these implementations, this compiler configuration, and the test computer. The benchmark does not prove that C is always faster or better for every task.
