from typing import TypeVar, List
from types import GenericAlias


T = TypeVar("T")
O = TypeVar("O")


def is_primitive(t: T) -> bool:
    """checks whether the type of `t` is one of the primitive types in python

    Args:
        t (any): the type or value to be checked

    Returns:
        bool: `True` if t is of primitive type, `False` if not
    """

    if isinstance(t, GenericAlias):
        t = t.__origin__

    if not isinstance(t, type):
        t = type(t)

    return t in (
        int,
        float,
        str,
        bool,
        list,
        tuple,
        dict,
        set,
    )


def is_number(t: T) -> bool:
    """checks whether the type of `t` is a primitive number type.
    this includes:
    - int
    - float

    Args:
        t (any): the type or value to be checked

    Returns:
        bool: `True` if t is of a primitive number type, `False` if not
    """

    if not isinstance(t, type):
        t = type(t)

    return t in (
        int,
        float,
    )


def is_container(t: T) -> bool:
    """checks whether the type of `t` is a primitive container type.
    this includes:
    - list
    - tuple
    - dict
    - set

    Args:
        t (any): the type or value to be checked

    Returns:
        bool: `True` if t is of a primitive container type, `False` if not
    """

    if isinstance(t, GenericAlias):
        t = t.__origin__

    if not isinstance(t, type):
        t = type(t)

    return t in (
        list,
        tuple,
        dict,
        set,
    )


def ensure_container(t: T) -> List[T]:
    """
    Ensures that the provided parameter is a container.

    Args:
        t: The parameter to be checked.

    Returns:
        A list containing the parameter if it is not already a container.
    """
    if not is_container(t):
        t = [t]

    return t


def any_type_of(t: T, o: O) -> bool:
    """checks whether `t` is of any type of `o`.
    this includes aliases, such as `list[int]`.
    this means that `any_type_of(list, list[int])` returns `True`

    Args:
        t (any): the value or type to be matched with `o`
        o (any): the value or type of origin

    Returns:
        bool: `True` if `t` is of any type of `o`, `False` if not
    """

    if isinstance(t, GenericAlias):
        t = t.__origin__
    if isinstance(o, GenericAlias):
        o = o.__origin__

    if not isinstance(t, type):
        t = type(t)
    if not isinstance(o, type):
        o = type(o)

    return t == o


def camel_to_snake(s: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        s (str): The camel case string to convert.

    Returns:
        str: The converted snake case string.

    Example:
        >>> camel_to_snake("camelCase")
        'camel_case'

    """
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def snake_to_camel(s: str) -> str:
    """
    Converts a snake_case string to camelCase.

    Args:
        s (str): The snake_case string to be converted.

    Returns:
        str: The camelCase string.

    Example:
        >>> snake_to_camel("hello_world")
        'helloWorld'
        >>> snake_to_camel("snake_case_example")
        'snakeCaseExample'
    """
    return "".join(c.capitalize() for c in s.lower().split("_"))


def snake_to_lower_camel(s: str) -> str:
    """
    Converts a snake_case string to lower camel case.

    Args:
        s: A snake_case string.

    Returns:
        A lower camel case representation of the input string.
    """
    camel_string = snake_to_camel(s)
    return s[0].lower() + camel_string[1:]
