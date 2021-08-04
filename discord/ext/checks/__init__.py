import logging
from functools import wraps
from typing import Awaitable, Callable


# consistency with the `discord` namespaced logging
log = logging.getLogger(__name__)


def add_listener_check(predicate: Awaitable[bool]) -> Callable:
    """
    Adds a check to an event listener
    Takes a coroutine which returns a predicate
    """

    def decorator(fn: Awaitable):
        @wraps(fn)
        async def check_predicate(*args, **kwargs):
            if await predicate(*args, **kwargs):
                await fn(*args, **kwargs)

        return check_predicate

    return decorator
