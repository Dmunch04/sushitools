# NOTE: experimental with the typing module (kinda sucks but it is cleaner)


from __future__ import annotations
from typing import TypeVar, Generic


T = TypeVar('T')


class InputRange(Generic[T]):
    @property
    def front(self) -> T:
        raise NotImplementedError

    def pop_front(self):
        raise NotImplementedError

    @property
    def empty(self) -> bool:
        raise NotImplementedError


class ForwardRange(Generic[T], InputRange[T]):
    @property
    def save(self) -> ForwardRange[T]:
        raise NotImplementedError


class BidirectionalRange(Generic[T], ForwardRange[T]):
    @property
    def save(self) -> BidirectionalRange[T]:
        raise NotImplementedError

    @property
    def back(self) -> T:
        raise NotImplementedError

    def pop_back(self):
        raise NotImplementedError


class InputAssignable(Generic[T], InputRange[T]):
    @property
    def set_front(self, val: T):
        raise NotImplementedError


class OutputRange(Generic[T]):
    def put(self, t: T):
        raise NotImplementedError