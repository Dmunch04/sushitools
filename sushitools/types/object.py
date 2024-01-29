from types import GenericAlias
from typing import TypeVar, Callable, Dict, Any
from ..json import JSONEncoder, JSONDecoder, default_encoder, default_decoder
from ..primitive import any_type_of, is_container, camel_to_snake, is_primitive

T = TypeVar("T")


__OBJECT_NAME = "__object_name__"
__OBJECT_FIELDS = "__object_fields__"
__OBJECT_FIELDS_LEN = "__object_fields_len__"
__OBJECT_KEY_MAPS = "__object_key_maps__"

__OBJECT_INIT_TEMPLATE = """\
def __init__(self, {args}):
{assignments}
"""


def __get_type_repr(t: type) -> str:
    if isinstance(t, GenericAlias):
        return f"{t.__origin__.__name__}[{', '.join(__get_type_repr(arg) for arg in t.__args__)}]"
    else:
        if not is_primitive(t):
            return "any"
        return t.__name__


# NOTE: access GenericAlias (ex. list[str]) param types using `t.__args__`


def is_object(cls: T) -> bool:
    """checks whether the given argument is an Object

    Args:
        cls (T): the class/type to check

    Returns:
        bool: `True` if the class/type has been given the `Object` decorator, `False` if not
    """

    return (
        hasattr(cls, __OBJECT_NAME)
        and hasattr(cls, __OBJECT_FIELDS)
        and hasattr(cls, __OBJECT_FIELDS_LEN)
    )


class ObjectField(object):
    __slots__ = ("name", "field_type", "default_value", "initialized")

    def __init__(
        self,
        name: str,
        field_type: type,
        default_value: any = None,
        initialized: bool = False,
    ):
        self.name = name
        self.field_type = field_type
        self.default_value = default_value
        self.initialized = initialized

    def get_value(self, cls: T) -> any:
        """finds the value of a specific field in an Object class instance

        Args:
            cls (T): the Object instance to look for the field value in

        Returns:
            any: the value of the field or `None` if field is not found
        """

        global __OBJECT_FIELDS
        if not is_object(cls):
            raise Exception("cannot find field value on non Object class")

        return getattr(cls, self.name, None)


def fields(cls: T) -> list[ObjectField]:
    """finds all the fields of that Object class/instance

    Args:
        cls (T): the Object class/instance to find fields of

    Returns:
        List[ObjectField]: a list of all fields the class contains

    """

    if not is_object(cls):
        raise Exception("cannot find fields on non Object class")

    return [field for field in getattr(cls, __OBJECT_FIELDS).values()]


def __to_json(
    self: T,
    *,
    encoder: JSONEncoder = default_encoder(),
    key_mangler: Callable[[str], str] = lambda x: x,
    skip_null: bool = False,
    use_default_value: bool = False,
    **kwargs,
) -> str:
    if not is_object(self):
        raise Exception("cannot encode non Object class to json")

    return encoder.encode(
        __to_dict(self, skip_null=skip_null, use_default_value=use_default_value),
        **kwargs,
    )


def __from_json(
    cls: T,
    data: str | dict[str, any],
    *,
    decoder: JSONDecoder = default_decoder(),
    key_demangler: Callable[[str], str] = camel_to_snake,
    **kwargs,
) -> T:
    if not is_object(cls):
        raise Exception("cannot decode non Object class from json")

    # TODO: this is a classmethod, meaning that it can also be called on an instance object; what do we do when that happens?

    if isinstance(data, str):
        data = decoder.decode(data, **kwargs)

    f = getattr(cls, __OBJECT_FIELDS)
    key_maps = getattr(cls, __OBJECT_KEY_MAPS, {})

    args: dict[str, str] = {}
    for key, value in data.items():
        key = key_maps.get(key, key_demangler(key))

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
        if is_container(field.field_type):
            sub_types: tuple[type] = field.field_type.__args__
            if not isinstance(value, (list, dict)):
                raise Exception()
            if isinstance(value, list):
                final: list[any] = []
                if len(sub_types) == 1:
                    typ: type = sub_types[0]
                    for val in value:
                        if is_object(typ):
                            final.append(typ.from_json(val))
                else:
                    print("fuck")

                print(final)
                value = str(final)
            elif isinstance(value, dict):
                if len(sub_types) != 2:
                    raise Exception()
                key_type, value_type = sub_types[0], sub_types[1]
                value = {__from_json(key_type, k): __from_json(value_type, v) for k, v in value.items()}
            else:
                raise Exception()
        elif not any_type_of(value, field.field_type):
            raise Exception(
                "%s Object field '%s' must be of type '%s'"
                % (getattr(cls, __OBJECT_NAME), key, __get_type_repr(field.field_type))
            )
        if field.field_type is str:
            value = '"%s"' % str(value)
        elif is_object(field.field_type):
            value = "%s.from_json(%s)" % (field.field_type, str(value))
        args[key] = str(value)

    instantiate_call = "res = OBJECT({args})".format(
        args=", ".join([f"{key}={value}" for key, value in args.items()])
    )

    namespace = dict(__name__="object_%s_from_json" % cls.__name__)
    namespace["OBJECT"] = cls
    exec(instantiate_call, namespace)
    return namespace["res"]


def __to_dict(
    self: T, *, skip_null: bool = False, use_default_value: bool = False
) -> dict[str, any]:
    if not is_object(self):
        raise Exception("cannot turn non Object class into dict")

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


def __copy_from(self: T, other: T):
    if not is_object(self):
        raise Exception("cannot copy to non Object class")
    if not is_object(other):
        raise Exception("cannot copy from non Object class")

    other_fields: list[ObjectField] = fields(other)
    for field in other_fields:
        setattr(self, field.name, field.get_value(other))


def __of(other: T):
    if not is_object(other):
        raise Exception("cannot copy from non Object class")

    t = type(other)()
    __copy_from(t, other)
    return t


def __load_json(self: T, data: str | dict[str, any], *, decoder: JSONDecoder = default_decoder(), **kwargs):
    if not is_object(self):
        raise Exception("cannot decode non Object class from json")

    if isinstance(data, str):
        data = decoder.decode(data, **kwargs)

    f: list[ObjectField] = getattr(self, __OBJECT_FIELDS)

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
                setattr(self, field.name, None)
            else:
                setattr(self, field.name, field.default_value)
            continue
        # TODO: do type checking on containers; fx list[int] -> all elements should be int
        if not any_type_of(value, field.field_type):
            raise Exception(
                "%s Object field '%s' must be of type '%s'"
                % (getattr(self, __OBJECT_NAME), key, __get_type_repr(field.field_type))
            )
        setattr(self, field.name, value)


def __make_constructor(cls: T) -> Callable:
    if not is_object(cls):
        raise Exception("cannot make constructor for non Object class")

    f: list[ObjectField] = fields(cls)

    init_def = __OBJECT_INIT_TEMPLATE.format(
        args=", ".join(
            [f"{field.name}: {__get_type_repr(field.field_type)} = {f'"{field.default_value}"' if field.field_type == str else field.default_value if field.default_value else "None"}" for field in f]
        ),
        assignments="\n".join([f"\tself.{field.name} = {field.name}" for field in f]),
    )

    print(init_def)

    namespace = dict(__name__="object_%s_init" % cls.__name__)
    exec(init_def, namespace)
    return namespace["__init__"]


def __process_attrs(cls: T):
    setattr(
        cls,
        __OBJECT_NAME,
        str(cls).replace("<", "").replace(">", "").replace("'", "").split(".")[-1],
    )
    setattr(
        cls,
        __OBJECT_KEY_MAPS,
        {}
    )


def __process_fields(cls: T):
    fields: dict[Any, ObjectField] = {}
    for key, ftype in getattr(cls, "__annotations__").items():
        df = getattr(cls, str(key), None)
        if not is_primitive(ftype):
            fields[key] = ObjectField(key, ftype, None, False)
        else:
            fields[key] = ObjectField(key, ftype, df or ftype(), df is not None)

    setattr(cls, __OBJECT_FIELDS, fields)
    setattr(cls, __OBJECT_FIELDS_LEN, len(fields))


def keymap(in_key: str, out_key: str) -> T:
    def wrapper(cls: T) -> T:
        if not is_object(cls):
            raise Exception()

        field_names = [field.name for field in fields(cls)]
        if out_key not in field_names:
            raise Exception()

        key_maps = getattr(cls, __OBJECT_KEY_MAPS, {})
        key_maps[in_key] = out_key
        setattr(cls, __OBJECT_KEY_MAPS, key_maps)

        return cls
    return wrapper


def Object(cls: T) -> T:
    """
    This is the main Object decorator function.

    This function checks if a passed in class is of type 'cls'. If not, an exception is thrown.

    After the type check, the processed class is enriched with additional attributes and methods
    which provide JSON and dictionary conversions, along with a new constructor. These are achieved
    by extending the behavior of the class via the `setattr` method.

    The Object decorator is intended to enhance your class by injecting these predefined methods for
    common operations.

    Parameters
    ----------
    cls: type
        A class to be processed. The class type is generic and is signified as 'T'.

    Returns
    -------
    T: type
        The enriched class with additional methods and attributes.

    Raises
    ------
    Exception:
        An exception is raised if the passed object is not a class.
    """
    if not isinstance(cls, type):
        raise Exception("Object decorator can only be used on class object")

    __process_attrs(cls)
    __process_fields(cls)

    setattr(cls, "__init__", __make_constructor(cls))
    setattr(cls, "to_json", __to_json)
    setattr(cls, "from_json", classmethod(__from_json))
    setattr(cls, "to_dict", __to_dict)
    setattr(cls, "copy_from", __copy_from)
    setattr(cls, "of", staticmethod(__of))
    setattr(cls, "load_json", __load_json)

    return cls
