from sushitools.decorators import deprecated, returns, arg, posarg


def test_deprecated():
    @deprecated(message="This is a deprecated message")
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)


def test_returns():
    @returns(int)
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)

    @returns(type(None))
    def nop() -> None:
        pass

    nop()


def test_arg() -> None:
    @arg("name", str)
    def greet(*, name: str) -> str:
        return f"Hello, {name}!"

    greet(name="Bob")


def test_posarg() -> None:
    @arg("a", int)
    def add(a: int, b: int) -> int:
        return a + b

    add(1, "2.0")
