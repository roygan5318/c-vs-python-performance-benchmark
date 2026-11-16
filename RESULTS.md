# Benchmark Results

Each value is the median of 10 runs. C was compiled with `cc -O2`.
Only the insertion-sort operation was timed.

| Array size | C median (seconds) | Python median (seconds) | Python/C ratio |
|---:|---:|---:|---:|
| 1,000 | 0.000093 | 0.039309 | 422.7× |
| 2,000 | 0.000392 | 0.165946 | 423.9× |
| 4,000 | 0.001615 | 0.738893 | 457.7× |
| 8,000 | 0.006722 | 2.638702 | 392.5× |

![Runtime graph](results.svg)

## Interpretation

Both implementations use the same O(n²) insertion-sort algorithm, so their runtimes grow similarly as the input gets larger. The absolute times differ because optimized C is compiled to native machine code, while CPython performs additional interpreter, dynamic-type, and object-handling work.
