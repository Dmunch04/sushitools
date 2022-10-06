from types import GenericAlias


def is_primitive(t: any) -> bool:
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


def is_number(t: any) -> bool:
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


def is_container(t: any) -> bool:
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


def any_type_of(t: any, o: any) -> bool:
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
