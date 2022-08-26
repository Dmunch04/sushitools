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