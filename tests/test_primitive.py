from sushitools import is_primitive, is_number, is_container


def test_is_primitive():
    assert is_primitive(1) and is_primitive(int)
    assert is_primitive(1.0) and is_primitive(float)
    assert is_primitive("hello") and is_primitive(str)
    assert is_primitive(True) and is_primitive(bool)
    assert is_primitive([1, 2, 3]) and is_primitive(list) and is_primitive(list[int])
    assert is_primitive((1, "2")) and is_primitive(tuple) and is_primitive(tuple[int, str])
    assert is_primitive({"1": "2"}) and is_primitive(dict) and is_primitive(dict[str, str])
    assert is_primitive({1, "2"}) and is_primitive(set) and is_primitive(set[int, str])

    class Holder:
        pass

    assert not is_primitive(Holder()) and not is_primitive(Holder)


def test_is_number():
    assert is_number(1) and is_number(int)
    assert is_number(1.0) and is_number(float)

    class Double(float):
        pass

    assert not is_number(Double()) and not is_number(Double)


def test_is_container():
    assert is_container([1, 2, 3]) and is_container(list) and is_container(list[int])
    assert is_container((1, "2")) and is_container(tuple) and is_container(tuple[int, str])
    assert is_container({"1": "2"}) and is_container(dict) and is_container(dict[str, str])
    assert is_container({1, "2"}) and is_container(set) and is_container(set[int, str])

    class Container(dict):
        pass

    assert not is_container(Container()) and not is_container(Container)