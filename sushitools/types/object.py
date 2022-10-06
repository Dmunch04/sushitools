from types import GenericAlias
from ..json import JSONEncoder, JSONDecoder, default_encoder, default_decoder
from ..primitive import any_type_of


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

    return [field for field in getattr(cls, __OBJECT_FIELDS).values()]


def to_json(self: type, *, encoder: JSONEncoder = default_encoder(), pretty: bool = False, skip_null: bool = False, use_default_value: bool = False, **kwargs) -> str:
    kwa = {**kwargs}
    if pretty:
        # TODO: what if another hook/encoder does not accept the "indent" arg?
        # NOTE: current solution to above is allowing user to specify own kwargs. so perhaps this pretty arg is not needed
        kwa["indent"] = 4

    return encoder.encode(to_dict(self, skip_null=skip_null, use_default_value=use_default_value), **kwa)


def from_json(cls: type, data: str | dict[str, any], *, decoder: JSONDecoder = default_decoder(), **kwargs) -> type:
    # TODO: this is a classmethod, meaning that it can also be called on an instance object; what do we do when that happens?

    if isinstance(data, str):
        data = decoder.decode(data, **kwargs)

    f = getattr(cls, __OBJECT_FIELDS)

    args: dict[str, str] = {}
    for key, value in data.items():
        field = f.get(key, None)
        if field is None:
            continue
        elif value is None:
            # TODO: NOTE: hmm perhaps this check should be outside this dict? so if the key wasn't in the given data
            # ^ then we should check it. because if the key was in data and value is None/null, then shouldn't that
            # ^ override the default value, compared to if None/null wasn't provided in the data. to clarify: if `data`
            # ^ contains "key" with value of "None" then the field should be set to "None". if `data` on the other hand
            # ^ did not contain "key" then the "key" field should become ("key").default_value
            if not field.initialized:
                args[key] = "None"
            else:
                args[key] = str(field.default_value)
            continue
        # TODO: do type checking on containers; fx list[int] -> all elements should be int
        if not any_type_of(value, field.ftype):
            raise Exception("%s Object field '%s' must be of type '%s'" % (getattr(cls, __OBJECT_NAME), key, __get_type_repr(field.ftype)))
        if field.ftype is str:
            value = '"%s"' % str(value)
        args[key] = str(value)

    instantiate_call = "res = OBJECT({args})".format(
        args=", ".join([f"{key}={value}" for key, value in args.items()])
    )

    namespace = dict(__name__="object_%s_from_json" % cls.__name__)
    namespace["OBJECT"] = cls
    exec(instantiate_call, namespace)
    return namespace["res"]


def to_dict(self: type, *, skip_null: bool = False, use_default_value: bool = False) -> dict[str, any]:
    d = {}
    for key, field in getattr(self, __OBJECT_FIELDS).items():
        val = getattr(self, field.name, None)
        if val is None:
            if skip_null:
                continue
            elif use_default_value:
                val = field.default_value
        if any_type_of(val, set):
            val = list(val)
        d[key] = val

    return d


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
        raise Exception("Object decorator can only be used on class object")

    __process_attrs(cls)
    __process_fields(cls)

    setattr(cls, "__init__", make_constructor(cls))
    setattr(cls, "to_json", to_json)
    setattr(cls, "from_json", classmethod(from_json))
    setattr(cls, "to_dict", to_dict)

    return cls
