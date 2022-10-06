from sushitools.types import Object, fields, is_object
from sushitools import is_primitive
#from sushitools.json import to_json, JSONValue
from json import dumps
import time


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
    #print(to_json(a.to_json()))

    #print(is_object(Person))
    #print(is_object(a))

    """
    d = {"name": "Daniel", "age": 18.51384931, "family": [{"name": "Kenneth", "age": 46}, {"name": "Pernille", "age": 45}]}
    val = JSONValue(d)

    print("beginning std json encode test...")
    start = time.time()
    res1 = dumps(d)
    end1 = time.time() - start

    print("beginning sushi json encode test...")
    start = time.time()
    res2 = to_json(val)
    end2 = time.time() - start

    print(f"std encode finished in {str(end1)}ms with result: {res1}")
    print(f"sushi encode finished in {str(end2)}ms with result: {res2}")
    """

    """
    for field in fields(Person):
        print(field.name, field.ftype, field.default_value, field.initialized, is_primitive(field.ftype))

    print(is_primitive(Person))
    print(is_primitive(int))
    print(is_primitive(1))

    class test:
        __slots__ = ("a", "b", "c")

        def __init__(self, *args):
            if len(args) == 1:
                if isinstance(args[0], dict):
                    pass
            else:
                for arg in args:
                    #setattr(self, )
                    pass
    """