# Same Algorithm, Different Speed: C vs. Python

This project benchmarks equivalent insertion-sort implementations in C and Python. It asks:

> When C and Python implement the same O(n²) algorithm, how do their execution times compare as the input size increases?

## Project contents

- `insertion_sort.c`: C implementation of insertion sort
- `insertion_sort.py`: Python implementation of the same algorithm
- `builtin_sort.py`: exploratory test using Python's native `sorted()` function
- `benchmark.py`: compiles C, creates identical inputs, runs repeated trials, and reports medians
- `results.csv`: measurements from the latest benchmark run
- `RESULTS.md`: formatted results and interpretation
- `results.svg`: graph of median execution time
- `presentation/`: presentation materials for the project

## What the project controls

- Both programs implement the same insertion-sort algorithm.
- Both receive the exact same randomly generated arrays.
- Array creation, file reading, output, and process startup are excluded from the measured time.
- Every result is checked for correct sorted order and matching checksums.
- The runner rotates which implementation runs first and reports the median of repeated trials.
- Each implementation receives one unmeasured warm-up run, and the measured run order rotates to reduce systematic ordering bias.
- The C program is compiled with `-O2`; this is disclosed because optimization affects performance.

The first two implementations are the fair experiment because both use insertion sort. The built-in `sorted()` result is reported separately: it uses CPython's native Timsort implementation, so it demonstrates the benefit of optimized library functions but is not an equivalent-algorithm comparison.

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

## Latest results

| Array size | C median | Python median | Python/C ratio |
|---:|---:|---:|---:|
| 1,000 | 0.000093 s | 0.039309 s | 422.7× |
| 2,000 | 0.000392 s | 0.165946 s | 423.9× |
| 4,000 | 0.001615 s | 0.738893 s | 457.7× |
| 8,000 | 0.006722 s | 2.638702 s | 392.5× |

These measurements came from one computer and one set of implementations. Results will vary across systems.

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

Big-O describes how work grows with input size; it does not predict the exact number of seconds. Both insertion-sort versions are O(n²), but C is expected to have a smaller constant factor because it is compiled to native instructions. CPython executes bytecode and performs dynamic type and object handling during each operation.

Python's `sorted()` function is implemented in CPython's native runtime and uses an O(n log n) algorithm. It can be dramatically faster than a loop written in Python because one Python call hands the entire operation to optimized native code. Its different algorithm means it must be treated as a separate exploration rather than evidence that the Python and C insertion-sort implementations are equivalent.

The conclusion should be limited to this algorithm, these implementations, this compiler configuration, and the test computer. The benchmark does not prove that C is always faster or better for every task.
