from types import GenericAlias
#from ..json import JSONValue
from ..primitive import is_primitive


__OBJECT_NAME = "__object_name__"
__OBJECT_FIELDS = "__object_fields__"
__OBJECT_FIELDS_LEN = "__object_fields_len__"

__OBJECT_INIT_TEMPLATE = """\
def __init__(self, {args}):
{assignments}
"""

def __get_type_repr(t: type):
    if isinstance(t, GenericAlias):
        return str(t)
    else:
        return t.__name__


# NOTE: access GenericAlias (ex. list[str]) param types using `t.__args__`


class ObjectField(object):
    __slots__ = ("name", "ftype", "default_value", "initialized")

    def __init__(self, name: str, ftype: type, default_value: any = None, initialized: bool = False):
        self.name = name
        self.ftype = ftype
        self.default_value = default_value
        self.initialized = initialized

        
def is_object(cls: type) -> bool:
    return hasattr(cls, __OBJECT_NAME) and hasattr(cls, __OBJECT_FIELDS) and hasattr(cls, __OBJECT_FIELDS_LEN)


def fields(cls: type) -> list[ObjectField]:
    if not is_object(cls):
        raise Exception("cannot find fields on non Object class")

    fields = []
    for key, field in getattr(cls, __OBJECT_FIELDS).items():
        fields.append(field)

    return fields


def to_json(self: type) -> str:
    """
    data = {}
    for field in fields(self):
        if field.ftype in (int, float, str, bool, list, dict):
            data[field.name] = getattr(self, field.name, field.default_value)
        elif is_object(field.ftype):
            df = getattr(self, field.name, None)
            if df is None:
                data[field.name] = {}
            else:
                data[field.name] = df.to_json()
        else:
            df = getattr(self, field.name, None)
            if df is not None:
                if hasattr(df, "to_json"):
                    try:
                        data[field.name] = df.to_json()
                    except:
                        raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
                elif hasattr(df, "toJson"):
                    try:
                        data[field.name] = df.toJson()
                    except:
                        raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
                elif hasattr(df, "json"):
                    try:
                        data[field.name] = df.json()
                    except:
                        raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
            else:
                # are there other cases we want to catch?
                raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
    """
    """
    data = {}
    for field in fields(self):
        if is_primitive(field.ftype):
            data[field.name] = JSONValue(getattr(self, field.name, field.default_value))
        elif is_object(field.ftype):
            df = getattr(self, field.name, None)
            if df is None:
                data[field.name] = JSONValue({})
            else:
                data[field.name] = df.to_json()
        else:
            df = getattr(self, field.name, None)
            if df is not None:
                if hasattr(df, "to_json"):
                    try:
                        data[field.name] = df.to_json()
                    except:
                        raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
                elif hasattr(df, "toJson"):
                    try:
                        data[field.name] = df.toJson()
                    except:
                        raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
                elif hasattr(df, "json"):
                    try:
                        data[field.name] = df.json()
                    except:
                        raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
            else:
                # are there other cases we want to catch?
                raise Exception("cannot convert field %s of type %s to json" % (field.name, str(field.type)))
    
    return JSONValue(data)
    """
    return ""


def make_constructor(cls: type):
    if not is_object(cls):
        raise Exception("cannot make constructor for non Object class")

    f: list[ObjectField] = fields(cls)

    init_def = __OBJECT_INIT_TEMPLATE.format(
        args=", ".join([f"{field.name}: {__get_type_repr(field.ftype)} = None" for field in f]),
        assignments='\n'.join([f"\tself.{field.name} = {field.name}" for field in f]),
    )

    namespace = dict(__name__="object_%s_init" % cls.__name__)
    exec(init_def, namespace)
    return namespace["__init__"]


def __process_attrs(cls: type):
    setattr(cls, __OBJECT_NAME, str(cls).replace("<", "").replace(">", "").replace("'", "").split(".")[-1])


def __process_fields(cls: type):
    fields = {}
    for key, ftype in getattr(cls, "__annotations__").items():
        df = getattr(cls, str(key), None)
        fields[key] = ObjectField(key, ftype, df or ftype(), df is not None)

    setattr(cls, __OBJECT_FIELDS, fields)
    setattr(cls, __OBJECT_FIELDS_LEN, len(fields))


def Object(cls):
    if not isinstance(cls, type):
        raise Exception("struct decorator can only be used on class object")

    __process_attrs(cls)
    __process_fields(cls)

    setattr(cls, "__init__", make_constructor(cls))
    setattr(cls, "to_json", to_json)

    return cls