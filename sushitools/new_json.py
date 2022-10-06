from __future__ import annotations
from enum import IntEnum
from types import GenericAlias


class JSONType(IntEnum):
    NULL = 0
    STRING = 1
    INTEGER = 2
    FLOAT = 3
    ARRAY = 4 # list[JSONValue]
    OBJECT = 5 # dict[str, JSONValue]
    TRUE = 6
    FALSE = 7


class JSONValue:
    def __init__(self, value: any):
        self.__value = value

        t: type = type(value)
        if t is type(None):
            self.__type_tag = JSONType.NULL
        elif t is str:
            self.__type_tag = JSONType.STRING
        elif t is bool:
            self.__type_tag = JSONType.TRUE if value else JSONType.FALSE
        elif t is int:
            self.__type_tag = JSONType.INTEGER
        elif t is float:
            self.__type_tag = JSONType.FLOAT
        elif t is dict:
            self.__type_tag = JSONType.OBJECT
            obj: dict[str, JSONValue] = {}
            for key, val in value.items():
                assert type(key) is str, "dict/object key should be a string"
                if type(val) is JSONValue:
                    obj[key] = val
                else:
                    obj[key] = JSONValue(val)
            self.__value = obj
        elif t is list or t is tuple:
            self.__type_tag = JSONType.ARRAY
            arr: list[JSONValue] = []
            for val in value:
                if type(val) is JSONValue:
                    arr.append(val)
                else:
                    arr.append(JSONValue(val))
            self.__value = arr
        elif t is JSONValue:
            self.__value = value.value
            self.__type_tag = value.type_tag
        else:
            raise Exception("unable to convert type %s to json" % str(t))

    @property
    def value(self) -> any:
        return self.__value

    @property
    def type_tag(self) -> JSONType:
        return self.__type_tag

    @property
    def string(self) -> str:
        assert self.type_tag == JSONType.STRING, "JSONValue is not a string"
        return str(self.value)

    @property
    def integer(self) -> int:
        assert self.type_tag == JSONType.INTEGER, "JSONValue is not an integer"
        return int(self.value)

    @property
    def floating(self) -> float:
        assert self.type_tag == JSONType.FLOAT, "JSONValue is not a float"
        return float(self.value)

    @property
    def boolean(self) -> bool:
        if self.type_tag == JSONType.TRUE:
            return True
        elif self.type_tag == JSONType.FALSE:
            return False

        raise Exception("JSONValue is not a boolean")

    @property
    def object(self) -> dict[str, JSONValue]:
        assert self.type_tag == JSONType.OBJECT, "JSONValue is not an object"
        return self.value

    @property
    def array(self) -> list[JSONValue]:
        assert self.type_tag == JSONType.ARRAY, "JSONValue is not an array"
        return self.value

    @property
    def is_null(self) -> bool:
        return self.type_tag == JSONType.NULL

    def get(self, t: type) -> any:
        if isinstance(t, GenericAlias):
            t = t.__origin__

        if not isinstance(t, type):
            t = type(t)

        if t is str:
            return self.string
        elif t is bool:
            return self.boolean
        elif t is float:
            return self.floating
        elif t is int:
            return self.integer
        elif t is list or t is tuple:
            return self.array
        elif t is dict:
            return self.object

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, key: any) -> any:
        if self.type_tag == JSONType.ARRAY:
            assert type(key) is int, "key must be int for array values"
            return self.value[key]
        elif self.type_tag == JSONType.OBJECT:
            assert type(key) is str, "key must be str for object values"
            return self.value[key]
        else:
            raise Exception("get item can only be used on array and object JSONValue")

    def __setitem__(self, key: any, value: any) -> None:
        if self.type_tag == JSONType.ARRAY:
            assert type(key) is int, "key must be int for array values"
            if type(value) is JSONValue:
                self.value[key] = value
            else:
                self.value[key] = JSONValue(value)
        elif self.type_tag == JSONType.OBJECT:
            assert type(key) is str, "key must be str for object values"
            if type(value) is JSONValue:
                self.value[key] = value
            else:
                self.value[key] = JSONValue(value)
        else:
            raise Exception("set item can only be used on array and object JSONValue")

    def __delitem__(self, key: any) -> None:
        if self.type_tag == JSONType.ARRAY:
            assert type(key) is int, "key must be int for array values"
            del self.value[key]
        elif self.type_tag == JSONType.OBJECT:
            assert type(key) is str, "key must be str for object values"
            del self.value[key]
        else:
            raise Exception("del item can only be used on array and object JSONValue")

    def __contains__(self, item: any) -> bool:
        if self.type_tag == JSONType.OBJECT:
            return item in self.value.keys() or self.value.values()
        else:
            return item in self.value
