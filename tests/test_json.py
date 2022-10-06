import json
from sushitools.json import *


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
