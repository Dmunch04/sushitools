from __future__ import annotations
from enum import IntEnum
from types import GenericAlias

from json import loads

from .array import Appender
#from .types.object import is_object, fields


class JSONOptions(IntEnum):
    NONE = 0
    NOT_ESCAPE_BACKLASHES = 0 << 1


class JSONType(IntEnum):
    NULL = 0
    STRING = 1
    INTEGER = 2
    FLOAT = 3
    ARRAY = 4  # list[JSONValue]
    OBJECT = 5  # dict[str, JSONValue]
    TRUE = 6
    FALSE = 7


class JSONValue:
    __match_args__ = ("type_tag", "value")

    def __init__(self, value: any):
        self.assign(value)

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

    @classmethod
    def from_string(cls: JSONValue, value: str) -> str | JSONValue:
        if isinstance(cls, JSONValue):
            cls.assign(value)
            return value
        else:
            return JSONValue(value)

    @property
    def integer(self) -> int:
        assert self.type_tag == JSONType.INTEGER, "JSONValue is not an integer"
        return int(self.value)

    @classmethod
    def from_integer(cls: JSONValue, value: int) -> int | JSONValue:
        if isinstance(cls, JSONValue):
            cls.assign(value)
            return value
        else:
            return JSONValue(value)

    @property
    def floating(self) -> float:
        assert self.type_tag == JSONType.FLOAT, "JSONValue is not a float"
        return float(self.value)

    @classmethod
    def from_floating(cls: JSONValue, value: float) -> float | JSONValue:
        if isinstance(cls, JSONValue):
            cls.assign(value)
            return value
        else:
            return JSONValue(value)

    @property
    def boolean(self) -> bool:
        if self.type_tag == JSONType.TRUE:
            return True
        elif self.type_tag == JSONType.FALSE:
            return False

        raise Exception("JSONValue is not a boolean")

    @classmethod
    def from_boolean(cls: JSONValue, value: bool) -> bool | JSONValue:
        if isinstance(cls, JSONValue):
            cls.assign(value)
            return value
        else:
            return JSONValue(value)

    @property
    def object(self) -> dict[str, JSONValue]:
        assert self.type_tag == JSONType.OBJECT, "JSONValue is not an object"
        return self.value

    @classmethod
    def from_object(cls: JSONValue, value: dict[str, JSONValue]) -> dict[str, JSONValue] | JSONValue:
        if isinstance(cls, JSONValue):
            cls.assign(value)
            return value
        else:
            return JSONValue(value)

    @property
    def array(self) -> list[JSONValue]:
        assert self.type_tag == JSONType.ARRAY, "JSONValue is not an array"
        return self.value

    @classmethod
    def from_array(cls: JSONValue, value: list[JSONValue | any]) -> list[JSONValue] | JSONValue:
        if isinstance(cls, JSONValue):
            cls.assign(value)
            return value
        else:
            return JSONValue(value)

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

    def assign(self, value: any) -> None:
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

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, key: int | str) -> JSONValue:
        if self.type_tag == JSONType.ARRAY:
            assert type(key) is int, "key must be int for array values"
            return self.value[key]
        elif self.type_tag == JSONType.OBJECT:
            assert type(key) is str, "key must be str for object values"
            return self.value[key]
        else:
            raise Exception("get item can only be used on array and object JSONValue")

    def __setitem__(self, key: int | str, value: any) -> None:
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

    def __delitem__(self, key: int | str) -> None:
        if self.type_tag == JSONType.ARRAY:
            assert type(key) is int, "key must be int for array values"
            del self.value[key]
        elif self.type_tag == JSONType.OBJECT:
            assert type(key) is str, "key must be str for object values"
            del self.value[key]
        else:
            raise Exception("del item can only be used on array and object JSONValue")

    # TODO: this doesn't work because it matches raw value against JSONValue
    def __contains__(self, item: any) -> bool:
        if self.type_tag == JSONType.OBJECT:
            return item in self.value.keys() or self.value.values()
        else:
            return item in self.value

    def __str__(self) -> str:
        return to_json(self)

    # TODO: tf? how do we check array
    def __eq__(self, other: any) -> bool:
        if type(other) is JSONValue:
            if self.type_tag == JSONType.INTEGER:
                if other.type_tag == JSONType.INTEGER:
                    return self.value == other.value
                elif other.type_tag == JSONType.FLOAT:
                    pass
        else:
            return self.value == other

    def __add__(self, other: any) -> JSONValue:
        if self.type_tag == JSONType.ARRAY:
            valcpy = self.value
            if type(other) is JSONValue:
                valcpy.append(other)
            else:
                valcpy.append(JSONValue(other))
            return JSONValue(valcpy)
        else:
            return self.value.__add__(other)

    def __iadd__(self, other: any) -> None:
        if self.type_tag == JSONType.ARRAY:
            if type(other) is JSONValue:
                self.value.append(other)
            else:
                self.value.append(JSONValue(other))
        else:
            self.value = self.value.__add__(other)

    def wraps(self, t: type) -> any:
        #if not is_object(t):
            raise Exception("fuck you")


class JSONException(Exception):
    def __init__(self, msg: str, line: int, col: int):
        super().__init__(f"{msg} (line {str(line)}, col {str(col)})")


class JSONDecoder:
    pass


# TODO: NOTE: holy fuck this is slow; 6-7ms slower than std
class JSONEncoder:
    def __init__(self, root: JSONValue, pretty: bool = False, options: JSONOptions = JSONOptions.NONE):
        self.out = Appender[str]()
        self.root = root
        self.pretty = pretty
        self.options = options

    def encode(self) -> str:
        self.write_value(self.root, 0)
        return str(self.out)

    def put_tabs(self, indent_level: int):
        if self.pretty:
            for i in range(indent_level):
                self.out.put("    ")

    def put_eol(self):
        if self.pretty:
            self.out.put('\n')

    def put_char_eol(self, char: str):
        self.out.put(char)
        self.put_eol()

    def write_string(self, string: str):
        self.out.put('"')

        for char in string:
            match char:
                case '"':
                    self.out.put("\\\"")
                case '\\':
                    self.out.put("\\\\")
                case '/':
                    if not (self.options & JSONOptions.NOT_ESCAPE_BACKLASHES):
                        self.out.put('\\')
                    self.out.put('/')
                case '\b':
                    self.out.put("\\b")
                case '\f':
                    self.out.put("\\f")
                case '\n':
                    self.out.put("\\n")
                case '\r':
                    self.out.put("\\r")
                case '\t':
                    self.out.put("\\t")
                case _:
                    self.out.put(char)

        self.out.put('"')

    def write_value(self, value: JSONValue, indent_level: int):
        match value.type_tag:
            case JSONType.OBJECT:
                obj = value.object
                if not obj:
                    self.out.put("{}")
                else:
                    self.put_char_eol('{')
                    first: bool = True

                    for name, val in obj.items():
                        if not first:
                            self.put_char_eol(',')
                        first = False
                        self.put_tabs(indent_level + 1)
                        self.write_string(name)
                        self.out.put(':')
                        if self.pretty:
                            self.out.put(' ')
                        self.write_value(val, indent_level + 1)

                    self.put_eol()
                    self.put_tabs(indent_level)
                    self.out.put('}')

            case JSONType.ARRAY:
                arr = value.array
                if not arr:
                    self.out.put("[]")
                else:
                    self.put_char_eol('[')
                    for i, elem in enumerate(arr):
                        if i:
                            self.put_char_eol(',')
                        self.put_tabs(indent_level + 1)
                        self.write_value(elem, indent_level + 1)

                    self.put_eol()
                    self.put_tabs(indent_level)
                    self.out.put(']')

            case JSONType.STRING:
                self.write_string(value.string)

            case JSONType.INTEGER:
                self.out.put(str(value.integer))

            case JSONType.FLOAT:
                val: float = value.floating

                fmt: str = "%.18g" % val
                self.out.put(fmt)

                if not ('e' in fmt or '.' in fmt):
                    self.out.put(".0")

            case JSONType.TRUE:
                self.out.put("true")

            case JSONType.FALSE:
                self.out.put("false")

            case JSONType.NULL:
                self.out.put("null")


# NOTE: temporary method until own json parser is made
def load_json(src: str) -> JSONValue:
    return JSONValue(loads(src))


def to_json(root: JSONValue, pretty: bool = False, options: JSONOptions = JSONOptions.NONE) -> str:
    return JSONEncoder(root, pretty, options).encode()


# TODO: parse https://github.com/dlang/phobos/blob/master/std/json.d#L931
class JSONParser:
    def __init__(self, source: str):
        self.source = source

        self.root = JSONValue(None)

        self.depth = -1
        self.next = None
        self.line = 1
        self.col = 0

    def error(self, msg: str):
        raise JSONException(msg, self.line, self.col)

    def is_whitespace(self, ch: str) -> bool:
        return ch == 0 or ch == '\0' or ch.isspace()

    def pop_char(self) -> str:
        if not self.source:
            return None

        ch: str = self.source[0]
        self.source = self.source[1: -1]

        if ch == '\n':
            self.line += 1
            self.col = 0
        else:
            self.col += 1

        return ch

    def peek_char(self) -> str:
        if not self.next:
            if not self.source:
                return '\0'

            self.next = self.pop_char()

        return self.next

    def skip_whitespace(self):
        while True:
            ch: str = self.peek_char()
            if not (ch or ch.isspace()):
                return

    def get_char(self, skip_whitespace: bool = False) -> str:
        if skip_whitespace:
            self.skip_whitespace()

        ch: str
        if not self.next:
            ch = self.next
        else:
            ch = self.pop_char()

        return ch

    def check_char(self, ch: str, case_sensitive: bool = True, skip_whitespace: bool = True):
        if skip_whitespace:
            self.skip_whitespace()

        ch2: str = self.get_char()
        if not case_sensitive:
            ch2 = ch2.lower()

        if ch2 != ch:
            self.error(f"expected '{ch}' but found '{ch2}'")

    def test_char(self, ch: str, case_sensitive: bool = True, skip_whitespace: bool = True) -> bool:
        if skip_whitespace:
            self.skip_whitespace()

        ch2: str = self.peek_char()
        if not case_sensitive:
            ch2 = ch2.lower()

        if ch2 != ch:
            return False

        self.get_char()
        return True

    # https://github.com/dlang/phobos/blob/master/std/json.d#L1086
