from sushitools.types import Object, fields, is_object


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
