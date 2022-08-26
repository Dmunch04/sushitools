# TODO: find a somewhat nice solution to accessing private variables on the type to be extended (dunno if possible to find a nicer way than current)
def extend(typ: type, name: str = None, static: bool = False):
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