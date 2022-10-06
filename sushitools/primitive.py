from types import GenericAlias


def is_primitive(t: any) -> bool:
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
    if not isinstance(t, type):
        t = type(t)

    return t in (
        int,
        float,
    )


def is_container(t: any) -> bool:
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
    if isinstance(t, GenericAlias):
        t = t.__origin__
    if isinstance(o, GenericAlias):
        o = o.__origin__

    if not isinstance(t, type):
        t = type(t)
    if not isinstance(o, type):
        o = type(o)

    return t == o
