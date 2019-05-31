import time
from philiprehberger_timerfunc import timer, timed, benchmark, TimerResult, BenchmarkResult


def test_timer_context_manager():
    with timer() as t:
        time.sleep(0.01)
    assert t.elapsed > 0
    assert t.elapsed_ms > 0


def test_timer_result_str():
    result = TimerResult(elapsed=0.042)
    text = str(result)
    assert "ms" in text


def test_timed_decorator():
    @timed
    def fast_fn():
        return 42

    assert fast_fn() == 42


def test_timed_with_threshold():
    @timed(threshold_ms=10000)
    def fn():
        return "ok"

    assert fn() == "ok"


def test_benchmark_basic():
    def fn():
        return sum(range(100))

    result = benchmark(fn, iterations=10, warmup=2)
    assert isinstance(result, BenchmarkResult)
    assert result.iterations == 10
    assert len(result.timings_ms) == 10


def test_benchmark_stats():
    def fn():
        time.sleep(0.001)

    result = benchmark(fn, iterations=5, warmup=1)
    assert result.mean_ms > 0
    assert result.median_ms > 0
    assert result.min_ms > 0
    assert result.max_ms >= result.min_ms
    assert result.p95_ms > 0
    assert result.total_ms > 0


def test_benchmark_str():
    result = benchmark(lambda: None, iterations=10, warmup=0)
    text = str(result)
    assert "mean=" in text
    assert "iterations" in text


def test_timed_as_bare_decorator():
    @timed
    def fn():
        return "bare"

    assert fn() == "bare"


def test_timed_preserves_name():
    @timed
    def my_function():
        pass

    assert my_function.__name__ == "my_function"
