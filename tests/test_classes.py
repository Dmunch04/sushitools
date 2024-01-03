from sushitools.classes import singleton


def test_singleton():
    class A:
        pass

    a1 = A()
    a2 = A()
    assert id(a1) != id(a2)

    @singleton
    class B:
        pass

    b1 = B()
    b2 = B()
    assert id(b1) == id(b2)
