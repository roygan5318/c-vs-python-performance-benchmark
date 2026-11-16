# Benchmark Results

Each value is the median of 10 runs. C was compiled with `cc -O2`.
Only the insertion-sort operation was timed.

| Array size | C median (seconds) | Python median (seconds) | Python/C ratio |
|---:|---:|---:|---:|
| 1,000 | 0.000131 | 0.052762 | 404.3× |
| 2,000 | 0.000540 | 0.231096 | 428.0× |
| 4,000 | 0.002220 | 0.920016 | 414.4× |
| 8,000 | 0.009213 | 3.698762 | 401.5× |

![Runtime graph](results.svg)

## Interpretation

Both implementations use the same O(n²) insertion-sort algorithm, so their runtimes grow similarly as the input gets larger. The absolute times differ because optimized C is compiled to native machine code, while CPython performs additional interpreter, dynamic-type, and object-handling work.
