# philiprehberger-timerfunc

[![Tests](https://github.com/philiprehberger/py-timerfunc/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-timerfunc/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-timerfunc.svg)](https://pypi.org/project/philiprehberger-timerfunc/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-timerfunc)](https://github.com/philiprehberger/py-timerfunc/commits/main)

Measure execution time of any function.

## Installation

```bash
pip install philiprehberger-timerfunc
```

## Usage

### Context Manager

```python
from philiprehberger_timerfunc import timer

with timer() as t:
    do_work()
print(f"Took {t.elapsed_ms:.1f}ms")
```

### Decorator

```python
from philiprehberger_timerfunc import timed

@timed
def process_data():
    ...  # logs: "process_data took 42.3ms"

@timed(threshold_ms=100)
def api_call():
    ...  # only logs if slower than 100ms
```

### Benchmark

```python
from philiprehberger_timerfunc import benchmark

result = benchmark(my_function, args=(data,), iterations=1000)
print(f"Mean: {result.mean_ms:.2f}ms, P95: {result.p95_ms:.2f}ms")
print(f"Fastest: {result.fastest:.2f}ms, Slowest: {result.slowest:.2f}ms")
print(result)  # full stats summary
```

### Comparing benchmarks

```python
from philiprehberger_timerfunc import benchmark, compare_benchmarks

old = benchmark(old_impl, iterations=1000)
new = benchmark(new_impl, iterations=1000)

ratio = compare_benchmarks(new, old)
# ratio > 1 means `new` is faster than `old` (old took proportionally longer)
print(f"new is {ratio:.2f}x faster than old")
```

## API

| Function / Class | Description |
|------------------|-------------|
| `timer()` | Context manager returning `TimerResult` |
| `@timed` / `@timed(threshold_ms=0)` | Decorator logging execution time |
| `benchmark(fn, args, kwargs, iterations, warmup)` | Returns `BenchmarkResult` |
| `BenchmarkResult.fastest` | Duration of the fastest run (ms); alias of `min_ms` |
| `BenchmarkResult.slowest` | Duration of the slowest run (ms); alias of `max_ms` |
| `compare_benchmarks(a, b)` | Returns `b.mean / a.mean`; values > 1 mean `a` is faster |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-timerfunc)

🐛 [Report issues](https://github.com/philiprehberger/py-timerfunc/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-timerfunc/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
