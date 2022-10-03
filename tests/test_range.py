from sushitools.range import InputRange, is_input_range


def test():
    class A(InputRange[int]):
        def pop_front(self):
            pass

        @property
        def empty(self) -> bool:
            pass

        @property
        def front(self) -> int:
            pass

    assert is_input_range(A)