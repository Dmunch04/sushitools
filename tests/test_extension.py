from sushitools.extension import extension, extend
from sushitools.types import Object


def test_extend():
    @Object
    class Vector3:
        x: int = 0
        y: int = 0
        z: int = 0

    first_str: str = str(Vector3(1, 1, 1))

    @extend(Vector3, "__str__")
    def to_string(self: Vector3) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    second_str: str = str(Vector3(1, 1, 1))

    assert first_str != second_str
    assert second_str == "(1, 1, 1)"


def test_extension():
    @Object
    class Vector3:
        x: int = 0
        y: int = 0
        z: int = 0

    first_str: str = str(Vector3(1, 1, 1))

    @extension
    class MyExtension:
        @extend(Vector3, "__str__")
        def to_string(self: Vector3) -> str:
            return f"({self.x}, {self.y}, {self.z})"

    second_str: str = str(Vector3(1, 1, 1))

    assert first_str != second_str
    assert second_str == "(1, 1, 1)"
