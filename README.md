# philiprehberger-timerfunc

[![Tests](https://github.com/philiprehberger/py-timerfunc/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-timerfunc/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-timerfunc.svg)](https://pypi.org/project/philiprehberger-timerfunc/)
[![License](https://img.shields.io/github/license/philiprehberger/py-timerfunc)](LICENSE)

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
print(result)  # full stats summary
```

## API

- `timer()` — Context manager returning `TimerResult`
- `@timed` / `@timed(threshold_ms=0)` — Decorator logging execution time
- `benchmark(fn, args, kwargs, iterations, warmup)` — Returns `BenchmarkResult`

## License

MIT
