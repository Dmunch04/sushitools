import sys
import json
from typing import Callable


class JSONDecoder:
    def __init__(self, decode_fn: Callable[[str, ...], dict[str, any]]):
        self.__decode_fn = decode_fn

    def hook(self, decode_fn: Callable[[str, ...], dict[str, any]]):
        self.__decode_fn = decode_fn

    def decode(self, src: str, **kwargs) -> dict[str, any]:
        return self.__decode_fn(src, **kwargs)


class JSONEncoder:
    def __init__(self, encode_fn: Callable[[dict[str, any], ...], str]):
        self.__encode_fn = encode_fn

    def hook(self, encode_fn: Callable[[dict[str, any], ...], str]):
        self.__encode_fn = encode_fn

    def encode(self, src: dict[str, any], **kwargs) -> str:
        return self.__encode_fn(src, **kwargs)


__DEFAULT_DECODER: JSONDecoder = JSONDecoder(json.loads)
__DEFAULT_ENCODER: JSONEncoder = JSONEncoder(json.dumps)


# @property  - how?
def default_decoder() -> JSONDecoder:
    return __DEFAULT_DECODER


# @property  - how?
def default_encoder() -> JSONEncoder:
    return __DEFAULT_ENCODER


def parse_json(
    src: str, decode_fn: Callable[[str, ...], dict[str, any]] = None, **kwargs
) -> dict[str, any]:
    if decode_fn:
        return decode_fn(src, **kwargs)
    else:
        return default_decoder().decode(src, **kwargs)


def to_json(
    src: dict[str, any],
    encode_fn: Callable[[dict[str, any], ...], str] = None,
    **kwargs
) -> str:
    if encode_fn:
        return encode_fn(src, **kwargs)
    else:
        return default_encoder().encode(src, **kwargs)
