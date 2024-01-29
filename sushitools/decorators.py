from typing import Callable, Any, Type, Union, get_type_hints, NoReturn
import warnings


def deprecated(_func: Callable = None, *, message: str = "") -> Callable:
    """
    Args:
        _func: A callable function. This is an optional argument which represents the function that is being deprecated. If not provided, it is used as a decorator.
        message: A string. This is an optional argument which represents the deprecation message to be displayed when the function is called.

    Returns:
        decorator: A callable function. This is the decorator function used to mark a function as deprecated.

    Raises:
        RuntimeWarning: This is raised whenever the decorated function is called.

    Example usage:
        @deprecated
        def my_function():
            pass

        @deprecated(message="This function is no longer supported")
        def my_other_function():
            pass

    Note:
        The decorator function should be used to mark functions that are no longer supported or will be removed in future versions of the software.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            warnings.warn(f"Function {func.__name__} is deprecated. {message}", category=RuntimeWarning)
            return func(*args, **kwargs)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)


def is_instance_of_any_type(value: Any, types: Union[Type, tuple[Type, ...]]) -> bool:
    """
    Args:
        value: The value to check the type of.
        types: A single type or a tuple of types to check against.

    Returns:
        bool: True if the value is an instance of any of the specified types, False otherwise.
    """
    return isinstance(value, types)


def returns(expected_return_type: Type) -> Callable:
    """
    Decorator to enforce the return type of a function.

    Args:
        expected_return_type: The expected return type of the function.

    Raises:
        TypeError: If the actual return type of the function does not match the expected return type.

    Returns:
        The original function with enforced return type.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            value = func(*args, **kwargs)
            if not is_instance_of_any_type(value, expected_return_type):
                raise TypeError(
                    f"'{func.__name__}' is expected to return '{expected_return_type.__name__}' but returned '{type(value).__name__}'")
            return value
        return wrapper
    return decorator


def arg(name: str, expected_arg_type: Type) -> Callable:
    """
    Args:
        name: The name of the argument that the decorator will check for
        expected_arg_type: The expected type of the argument

    Returns:
        The decorator function

    Raises:
        ValueError: If the specified argument is missing
        TypeError: If the specified argument has a type that is not compatible with the expected_arg_type

    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            if name not in kwargs:
                raise ValueError(f"Argument '{name}' is missing.")
            value = kwargs[name]
            if not is_instance_of_any_type(value, expected_arg_type):
                raise TypeError(
                    f"Argument '{name}' is expected to be of type '{expected_arg_type.__name__}' but received '{type(value).__name__}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def posarg(index: int, expected_arg_type: Type) -> Callable:
    """
    Args:
        index: The index of the positional argument to check.
        expected_arg_type: The expected type of the positional argument.

    Returns:
        decorator: A decorator function.

    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            value = args[index]
            if not is_instance_of_any_type(value, expected_arg_type):
                raise TypeError(
                    f"Positional argument at index {index} is expected to be of type '{expected_arg_type.__name__}' but received '{type(value).__name__}'")
        return wrapper
    return decorator


def timer(callback: Callable[[str], NoReturn]) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            callback(str(elapsed_time))
            return result
        return wrapper
    return decorator
