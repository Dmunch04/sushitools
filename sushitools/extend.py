# TODO: find a somewhat nice solution to accessing private variables on the type to be extended (dunno if possible to find a nicer way than current)
def extend(typ: type, name: str = None, static: bool = False):
    """extends a function to a class type

    Args:
        typ (type): the class to be extended
        name (str, optional): the to be used when extending the function to the class. defaults to the functions own name.
        static (bool, optional): whether or not the function should be static. defaults to False.
    """

    def decorator(func):
        if not name:
            fname = func.__name__
        else:
            fname = name
        
        if static:
            setattr(typ, fname, staticmethod(func))
        else:
            setattr(typ, fname, func)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator