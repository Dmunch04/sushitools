import json
from sushitools.json import default_encoder, default_decoder
from sushitools.types import Object, fields, is_object, ObjectField


def test_INIT():
    default_encoder().hook(json.dumps)
    default_decoder().hook(json.loads)


def test_instance_from_json():
    @Object
    class Method:
        access_modifiers: int = 0
        return_type: str = "void"
        name: str = ""
        param_types: list[str] = []

    init_method: Method = Method(access_modifiers=21, return_type="void", name="init", param_types=["string", "string"])
    second_init_method: Method = Method.of(init_method)
    print(init_method.name)
    print(second_init_method.name)

    third_init_method = Method()
    third_init_method.load_json(init_method.to_json())
    print(third_init_method.name)


def test_struct():
    @Object
    class Person:
        name: str
        age: int
        other: float = 6.9
        smth: list[int]
        a: tuple[str]
        b: dict[str, any]
        c: set[any]
        d: bool
        e: list[list[int]]

    a: Person = Person(name="Daniel", d=True, e=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    data: str = a.to_json()
    b: Person = Person.from_json(data)
    assert b.name == a.name
    assert b.other == 6.9
    assert b.d
    assert len(b.e) == 3 == len(a.e)

    assert is_object(Person) and is_object(a) and is_object(b)

    b.name = "Bob"

    field: ObjectField = fields(Person)[0]
    assert field.get_value(a) == "Daniel"
    assert field.get_value(b) == "Bob"
