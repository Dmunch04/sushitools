from typing import TypeVar


T = TypeVar("T")


def singleton(cls: T):
    """
    Args:
        cls (Type[T]): The class to be turned into a singleton.

    Returns:
        T: The instance of the singleton class.

    """
    def wrapper(*args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    cls._instance = None
    return wrapper
