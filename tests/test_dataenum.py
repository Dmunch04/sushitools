from sushitools.types import dataenum


def test_dataenum():
    Gender = dataenum(
        "Gender", ("Male", "name", "age"), ("Female", "name", "age", "is_pregnant")
    )

    me = Gender.Male("munchii", 0)
    assert me.name == "munchii"
    assert me.age == 0

    some_man = Gender.Male("Torben", 49)
    assert some_man.name == "Torben"
    assert some_man.age == 49

    some_woman = Gender.Female("Bente", 37, False)
    assert some_woman.name == "Bente"
    assert some_woman.age == 37
    assert some_woman.is_pregnant == False

    assert me == some_man
    assert me != some_woman
