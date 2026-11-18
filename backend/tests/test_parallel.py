import threading
import time

import pytest

from workflows.parallel import run_parallel


def test_returns_results_by_name():
    results = run_parallel({"a": lambda: 1, "b": lambda: "two"})

    assert results == {"a": 1, "b": "two"}


def test_runs_tasks_concurrently():
    barrier = threading.Barrier(3, timeout=2)

    def task():
        # Only passes if all three tasks are running at the same time.
        barrier.wait()
        return True

    start = time.perf_counter()
    results = run_parallel({"a": task, "b": task, "c": task})

    assert all(results.values())
    assert time.perf_counter() - start < 2


def test_reraises_task_errors():
    def boom():
        raise ValueError("skill failed")

    with pytest.raises(ValueError, match="skill failed"):
        run_parallel({"ok": lambda: 1, "bad": boom})
