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
