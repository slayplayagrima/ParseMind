from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any


def run_parallel(tasks: dict[str, Callable[[], Any]]) -> dict[str, Any]:
    """
    Run independent tasks at the same time and return their results by name.

    The skills in a workflow each make their own LLM call and don't depend
    on each other, so running them together cuts total latency to roughly
    the slowest single call. If any task raises, the error is re-raised.
    """

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = {
            name: executor.submit(task)
            for name, task in tasks.items()
        }

        return {
            name: future.result()
            for name, future in futures.items()
        }
