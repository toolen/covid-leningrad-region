import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from mypy_extensions import KwArg, VarArg

default_logger = logging.getLogger(__name__)

# F = TypeVar("F", bound=Callable[..., Any])
ReturnType = TypeVar("ReturnType")


def retry_on_failure(
    num_of_retries: int = 3,
    interval_between_retries_sec: int = 5,
    logger: logging.Logger = default_logger,
) -> Callable[[Callable[..., ReturnType]], Callable[..., ReturnType]]:
    def decorator_retry(
        func: Callable[..., ReturnType]
    ) -> Callable[[VarArg(Any), KwArg(Any)], ReturnType]:
        @wraps(func)
        def wrapper_retry(*args: Any, **kwargs: Any) -> ReturnType:
            nonlocal num_of_retries
            while num_of_retries != 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    num_of_retries -= 1
                    time.sleep(interval_between_retries_sec)
                    logger.error(e)

        return wrapper_retry

    return decorator_retry
