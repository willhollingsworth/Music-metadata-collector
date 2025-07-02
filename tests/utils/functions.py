import inspect
from collections.abc import Callable
from typing import Any


def count_args(func: Callable[..., Any]) -> int:
    """Count the number of arguments in a function."""
    sig = inspect.signature(func)
    return len(sig.parameters)
