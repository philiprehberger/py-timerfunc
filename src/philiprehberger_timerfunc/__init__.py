"""Measure execution time of any function."""

from __future__ import annotations

import functools
import logging
import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Callable


__all__ = [
    "timer",
    "timed",
    "benchmark",
    "TimerResult",
    "BenchmarkResult",
]

logger = logging.getLogger(__name__)


@dataclass
class TimerResult:
    """Result from a timer context manager."""

    elapsed: float = 0.0
    """Elapsed time in seconds."""

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time in milliseconds."""
        return self.elapsed * 1000

    def __str__(self) -> str:
        if self.elapsed_ms < 1:
            return f"{self.elapsed * 1_000_000:.0f}\u00b5s"
        if self.elapsed_ms < 1000:
            return f"{self.elapsed_ms:.1f}ms"
        return f"{self.elapsed:.2f}s"


class timer:
    """Context manager for measuring execution time.

    Usage::

        with timer() as t:
            do_work()
        print(f"Took {t.elapsed_ms:.1f}ms")
    """

    def __init__(self) -> None:
        self.result = TimerResult()

    def __enter__(self) -> TimerResult:
        self._start = time.perf_counter()
        return self.result

    def __exit__(self, *args: Any) -> None:
        self.result.elapsed = time.perf_counter() - self._start


def timed(
    fn: Callable[..., Any] | None = None,
    *,
    threshold_ms: float = 0,
    name: str = "",
) -> Any:
    """Decorator to log execution time of a function.

    Can be used as ``@timed`` or ``@timed(threshold_ms=100)``.

    Args:
        fn: The function to decorate.
        threshold_ms: Only log if execution exceeds this threshold (ms).
            0 means always log.
        name: Custom name for log output. Defaults to function name.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        label = name or func.__qualname__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                if elapsed_ms >= threshold_ms:
                    logger.info("%s took %.1fms", label, elapsed_ms)

        return wrapper

    if fn is not None:
        return decorator(fn)
    return decorator


@dataclass
class BenchmarkResult:
    """Statistics from a benchmark run."""

    timings_ms: list[float] = field(default_factory=list)
    iterations: int = 0

    @property
    def mean_ms(self) -> float:
        return statistics.mean(self.timings_ms) if self.timings_ms else 0

    @property
    def median_ms(self) -> float:
        return statistics.median(self.timings_ms) if self.timings_ms else 0

    @property
    def min_ms(self) -> float:
        return min(self.timings_ms) if self.timings_ms else 0

    @property
    def max_ms(self) -> float:
        return max(self.timings_ms) if self.timings_ms else 0

    @property
    def stdev_ms(self) -> float:
        return statistics.stdev(self.timings_ms) if len(self.timings_ms) > 1 else 0

    @property
    def p95_ms(self) -> float:
        return _percentile(self.timings_ms, 0.95)

    @property
    def p99_ms(self) -> float:
        return _percentile(self.timings_ms, 0.99)

    @property
    def total_ms(self) -> float:
        return sum(self.timings_ms)

    def __str__(self) -> str:
        return (
            f"Benchmark ({self.iterations} iterations): "
            f"mean={self.mean_ms:.2f}ms, median={self.median_ms:.2f}ms, "
            f"min={self.min_ms:.2f}ms, max={self.max_ms:.2f}ms, "
            f"p95={self.p95_ms:.2f}ms, p99={self.p99_ms:.2f}ms"
        )


def benchmark(
    fn: Callable[..., Any],
    *,
    args: tuple = (),
    kwargs: dict[str, Any] | None = None,
    iterations: int = 100,
    warmup: int = 5,
) -> BenchmarkResult:
    """Run a function multiple times and collect timing statistics.

    Args:
        fn: The function to benchmark.
        args: Positional arguments for the function.
        kwargs: Keyword arguments for the function.
        iterations: Number of timed iterations.
        warmup: Number of warmup iterations (not timed).

    Returns:
        BenchmarkResult with timing statistics.
    """
    kwargs = kwargs or {}

    # Warmup
    for _ in range(warmup):
        fn(*args, **kwargs)

    timings: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        timings.append(elapsed)

    return BenchmarkResult(timings_ms=timings, iterations=iterations)


def _percentile(data: list[float], p: float) -> float:
    if not data:
        return 0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * p
    f = int(k)
    c = f + 1
    if c >= len(sorted_data):
        return sorted_data[-1]
    d = k - f
    return sorted_data[f] * (1 - d) + sorted_data[c] * d
