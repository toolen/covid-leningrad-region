"""This file contains decorators."""
import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar, cast

default_logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry_on_failure(
    num_of_retries: int = 3,
    interval_between_retries_sec: int = 30,
    logger: logging.Logger = default_logger,
) -> Callable[[F], F]:
    """
    Invoke decorated function in case of exception.

    :param num_of_retries:
    :param interval_between_retries_sec:
    :param logger:
    :return:
    """

    def decorator_retry(func: F) -> F:
        @wraps(func)
        def wrapper_retry(*args: Any, **kwargs: Any) -> Any:
            nonlocal num_of_retries
            while num_of_retries != 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    num_of_retries -= 1
                    time.sleep(interval_between_retries_sec)
                    logger.error(e)

        return cast(F, wrapper_retry)

    return decorator_retry
