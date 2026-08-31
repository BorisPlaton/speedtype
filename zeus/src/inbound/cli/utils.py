from functools import wraps
from typing import Callable

import uvloop


def async_command(command: Callable[[...], None]) -> Callable[[...], None]:

    @wraps(command)
    def wrapper(*args, **kwargs) -> None:
        uvloop.run(command(*args, **kwargs))

    return wrapper
