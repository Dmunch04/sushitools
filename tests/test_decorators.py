from sushitools.decorators import deprecated, returns, arg, posarg, timer


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
    #@arg("a", int)
    @posarg(0, int)
    @posarg(1, int)
    def add(a: int, b: int) -> int:
        return a + b

    add(1, "2.0")


def test_timer() -> None:
    @timer(print)
    def long_task():
        for i in range(100_000_000):
            pass

    long_task()


