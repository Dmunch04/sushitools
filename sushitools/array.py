from typing import TypeVar, Generic


T = TypeVar('T')


class Appender(Generic[T]):
    def __init__(self):
        self.__typ = T
        self.__data: list[T] = []

    @property
    def data(self) -> list[T]:
        return self.__data

    def put(self, t: T):
        if type(t) is self.__typ:
            self.__data.append(t)
        else:
            # TODO: hmm? type never matches because __typ is ~T?
            self.__data.append(t)

    def put_many(self, *t: T):
        for elem in t:
            self.put(elem)

    def __str__(self) -> str:
        return "".join([str(elem) for elem in self.__data])
