from typing import TypeVar, Callable


T = TypeVar("T")


__EMPTY_INIT_TEMPLATE = """\
def __init__(self):
    pass
"""


__INIT_TEMPLATE = """\
def __init__(self):
    raise Exception("extension class cannot be instantiated")
"""


def __make_constructor(cls: T, empty: bool = False) -> Callable:
    namespace = dict(__name__="extension_%s_init" % cls.__name__)
    exec(__EMPTY_INIT_TEMPLATE if empty else __INIT_TEMPLATE, namespace)
    return namespace["__init__"]


def extension(cls: T):
    """
    Args:
        cls (type): The class to apply the extension decorator to.

    Raises:
        TypeError: If the given cls is not a class.

    Example:
        # Apply extension decorator to MyClass
        @extension
        class MyClass:
            pass
    """
    if not isinstance(cls, type):
        raise TypeError("extension decorator can only be applied to classes")

    setattr(cls, "__init__", __make_constructor(cls, empty=True))
    _ = cls()
    setattr(cls, "__init__", __make_constructor(cls))


def extend(t: T, name: str = None, static: bool = False):
    """
    Args:
        t (T) : The class or object to extend.
        name (str, optional) : The name of the extended function. If not provided, the name of the decorated function will be used.
        static (bool, optional) : Determines whether the extended function should be static. Defaults to False.

    Returns:
        callable : The decorated function that will be added as an attribute to the provided class or object.

    Example usage:
        class MyClass:
            @extend(MyClass)
            def my_function(self):
                pass

        obj = MyClass()
        obj.my_function()
    """
    def decorator(func: Callable):
        fname = name or func.__name__
        func = staticmethod(func) if static else func
        setattr(t, fname, func)
        
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
