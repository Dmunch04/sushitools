from sushitools import extend
from sushitools.types import dataenum


def test_extend():
    Person = dataenum("Person", ("MALE", "name"), ("FEMALE", "name"))
    me: Person = Person.MALE("Daniel")

    assert str(me) == "Person.MALE(name)"

    @extend(Person)
    def get_instance_name(self: Person) -> str:
        return type(self.get_instance()).__name__.split("_")[-1]

    @extend(Person, name="__str__")
    def to_string(self: Person) -> str:
        return str(self.get_instance()).split("(")[0]

    assert str(me) == "Person.MALE"
    assert me.get_instance_name() == "MALE"


def test_extend_static():
    class Person(object):
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    @extend(Person, static=True)
    def new(name: str, age: int = 18):
        return Person(name, age)

    assert Person.new("Daniel").age == 18