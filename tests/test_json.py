import json
from sushitools.json import *

"""
def test_json_value():
    value1: JSONValue = JSONValue(None)
    value2: JSONValue = JSONValue("abc")
    value3: JSONValue = JSONValue(True)
    value4: JSONValue = JSONValue(False)
    value5: JSONValue = JSONValue(1)
    value6: JSONValue = JSONValue(1.0)
    value7: JSONValue = JSONValue({"name": "Daniel"})
    value8: JSONValue = JSONValue(["a", "b", "c"])
    value9: JSONValue = JSONValue(value1)

    assert value1.type_tag == JSONType.NULL
    assert value2.type_tag == JSONType.STRING
    assert value3.type_tag == JSONType.TRUE
    assert value4.type_tag == JSONType.FALSE
    assert value5.type_tag == JSONType.INTEGER
    assert value6.type_tag == JSONType.FLOAT
    assert value7.type_tag == JSONType.OBJECT
    assert value8.type_tag == JSONType.ARRAY
    assert value9.type_tag == value1.type_tag == JSONType.NULL

    assert value1.is_null and value9.is_null

    assert type(val := value2.get(str)) == str and val == "abc"
    assert type(val := value7.get(dict)) == dict and val == {"name": value7["name"]}

    assert value7["name"].string == "Daniel"
    assert value8[0].string == "a"

    match value5:
        case JSONValue(JSONType.FLOAT):
            print("FLOAT")
        case JSONValue(JSONType.INTEGER):
            print("INTEGER")
        case _:
            print("NONE OF ABOVE")

    assert len(value2) == 3

    value10: JSONValue = JSONValue.from_boolean(True)
    assert value10.boolean == True

    value11: JSONValue = JSONValue.from_array([1, 2, 3])
    assert value11.array == [1, 2, 3]
    #value11 += 4
    #print(value11.array)
    #assert value11.array == [1, 2, 3, 4]

    value12: JSONValue = JSONValue({"name": "Bob"})
    assert len(value12) == 1
    value12["age"] = 25
    assert len(value12) == 2
    assert value12["age"].integer == 25
"""

def test_json_decode():
    data = """\
{
    "name": "Daniel",
    "obj": {
        "key": "123",
        "value": true
    },
    "fl": 12.34
}
"""
    obj = parse_json(data)
    assert obj["name"] == "Daniel"
    assert obj["obj"]["key"] == "123"
    assert obj["obj"]["value"]
    assert obj["fl"] == 12.34

    def custom_decode_hook(src: str, **kwargs) -> dict[str, any]:
        res = json.loads(src)
        res["smth"] = "some value"
        return res

    custom_json_obj_1 = parse_json(data, decode_fn=custom_decode_hook)
    default_decoder().hook(custom_decode_hook)
    custom_json_obj_2 = parse_json(data)
    assert custom_json_obj_1 == custom_json_obj_1
    assert custom_json_obj_1["smth"] == "some value"


def test_json_encode():
    data = {
        "name": "Daniel",
        "obj": {
            "key": "123",
            "value": True
        },
        "fl": 12.34
    }

    json_str = to_json(data)
    assert len(json_str) == 69

    pretty_json_str = to_json(data, indent=4)
    assert len(pretty_json_str.split('\n')) == 8

    def custom_encode_hook(src: dict[str, any], **kwargs) -> str:
        return json.dumps(src) + "..."

    custom_json_str_1 = to_json(data, encode_fn=custom_encode_hook)
    default_encoder().hook(custom_encode_hook)
    custom_json_str_2 = to_json(data)
    assert custom_json_str_1 == custom_json_str_2
    assert custom_json_str_1.endswith("...")
