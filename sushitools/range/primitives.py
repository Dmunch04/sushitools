from typing import TypeVar
from .interfaces import *


T = TypeVar('T')


def is_input_range(t: T) -> bool:
    return (isinstance(t, InputRange) or issubclass(t, InputRange)) and (
        hasattr(t, "empty") and
        hasattr(t, "front") and
        hasattr(t, "pop_front")
    )


def is_output_range(t: T) -> bool:
    return (isinstance(t, OutputRange) or issubclass(t, OutputRange)) and (
        hasattr(t, "put")
    )