from enum import IntEnum
from .types import dataenum


class JsonElementType(IntEnum):
    STRING = 0
    INTEGER = 1
    FLOAT = 2
    NULL = 3
    TRUE = 4
    FALSE = 5
    ARRAY = 6
    OBJECT = 7


JsonValueType = dataenum("JsonValueType",
    "NULL",
    ("BOOLEAN", "boolean"),
    ("INTEGER", "integer"),
    ("FLOAT", "floating"),
    ("STRING", "string"),
    ("ARRAY", "array"),
    ("OBJECT", "object"),
)


class JsonValue:
    def __init__(self, value: JsonValueType):
        self.value = value

    def __getitem__(self, key):
        # TODO: array slicing doesnt work oof
        return self.value.match(
            (JsonValueType.ARRAY, lambda array: array.__getitem__(key)),
            (JsonValueType.OBJECT, lambda object: object.__getitem__(key)),
            default = lambda value: value.__getitem__(key)
        )

    def __setitem__(self, key, value):
        if self.value == JsonValueType.STRING:
            str_list = [*self.value.string]
            str_list.__setitem__(key, value)
            self.value = JsonValueType.STRING(''.join(str_list))
        elif self.value == JsonValueType.ARRAY:
            self.value.array.__setitem__(key, value)
        elif self.value == JsonValueType.OBJECT:
            self.value.object.__setitem__(key, value)
        else:
            raise Exception("cannot set item on json type %s" % str(self.value))

    def append(self, value: any):
        if self.value == JsonValueType.ARRAY:
            self.value.array.append(value)
        else:
            raise Exception("cannot append to non-array value")

    def put(self, key: str, value: any):
        if self.value == JsonValueType.OBJECT:
            self.value.object[str] = value
        else:
            raise Exception("cannot put into non-object value")


class JsonParserScope:
    def __init__(self, name: str = ""):
        self.name = name
        self.map: dict[str, JsonValueType] = {}

    def append(self, key: str, value: JsonValueType):
        self.map[key] = value


class JsonParser:
    def __init__(self, source: str):
        self.source = source

        self.index = 0
        self.start = 0
        self.current = 0
        self.line = 1

        self.in_array = False

        self.in_field = False
        self.field_name = ""

        # whenever we encounter a { or [ we add a new scope and then we can append the children elements to it before popping it
        self.scopes: list[JsonValueType] = []

    def parse(self) -> JsonValue:
        for char in self.source:
            if char == '{':
                self.scopes.append(JsonValueType.OBJECT({}))
            elif char == '[':
                self.scopes.append(JsonValueType.ARRAY([]))
                self.in_array = True
            elif char == '}':
                if self.in_field:
                    scope = self.scopes.pop()
                    self.scopes[-1].object(self.field_name, scope)
                #else:


        return self.scopes[0]

    def make_string(self):
        pass

    def make_number(self):
        pass

    def make_identifier(self):
        pass


class JsonTraverser:
    def __init__(self, source: str):
        self.source = source

        self.depth = -1
        self.start = 0
        self.current = 0

        self.start_cache = []
        self.scopes = []

        self.traverse()

    def traverse(self):
        for char in self.source:
            self.current += 1

            if char in ('{', '['):
                self.depth += 1
                self.start = self.current
                self.start_cache.append(self.start)
            elif char in ('}', ']'):
                start = self.start_cache.pop(self.depth)
                self.scopes.append((self.depth, self.source[start - 1 : self.current]))
                self.source = self.source[:start - 1] + self.source[self.current:]
                self.depth -= 1
                self.start = 0

        if not self.depth == -1:
            raise Exception("unterminated scope")


class NewJsonParser:
    def __init__(self, source: str):
        self.source = source

    def lex_string(self, string: str):
        json_string = ""

        if string[0] == "\"":
            string = string[1:]
        else:
            return None, string

        for c in string:
            if c == "\"":
                return json_string, string[len(json_string) + 1:]
            else:
                json_string += c

        raise Exception("unterminated string")


    def lex_number(self, string: str):
        json_number = ''

        number_characters = [str(d) for d in range(0, 10)] + ["-", "e", "."]

        for c in string:
            if c in number_characters:
                json_number += c
            else:
                break

        rest = string[len(json_number):]

        if not len(json_number):
            return None, string

        if '.' in json_number:
            return float(json_number), rest

        return int(json_number), rest

    TRUE_LEN = len("true")
    FALSE_LEN = len("false")
    NULL_LEN = len("null")

    def lex_bool(self, string: str):
        string_len = len(string)

        if string_len >= NewJsonParser.TRUE_LEN and \
            string[:NewJsonParser.TRUE_LEN] == 'true':
            return True, string[NewJsonParser.TRUE_LEN:]
        elif string_len >= NewJsonParser.FALSE_LEN and \
            string[:NewJsonParser.FALSE_LEN] == 'false':
            return False, string[NewJsonParser.FALSE_LEN:]

        return None, string


    def lex_null(self, string: str):
        string_len = len(string)

        if string_len >= NewJsonParser.NULL_LEN and \
            string[:NewJsonParser.NULL_LEN] == 'null':
            return True, string[NewJsonParser.NULL_LEN:]

        return None, string


    def lex(self):
        string = self.source
        tokens = []

        while len(string):
            json_string, string = self.lex_string(string)
            if json_string is not None:
                tokens.append(json_string)
                continue

            json_number, string = self.lex_number(string)
            if json_number is not None:
                tokens.append(json_number)
                continue

            json_bool, string = self.lex_bool(string)
            if json_bool is not None:
                tokens.append(json_bool)
                continue

            json_null, string = self.lex_null(string)
            if json_null is not None:
                tokens.append(None)
                continue

            c = string[0]

            if c in [' ', '\t', '\b', '\n', '\r']:
                # Ignore whitespace
                string = string[1:]
            elif c in [',', ':', '[', ']', '{', '}', '"']:
                tokens.append(c)
                string = string[1:]
            else:
                raise Exception('Unexpected character: {}'.format(c))

        return tokens