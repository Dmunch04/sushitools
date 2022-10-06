import sys
import json
from typing import Callable


class JSONDecoder:
    """the base class for sushitools json decoders"""

    def __init__(self, decode_fn: Callable[[str, ...], dict[str, any]]):
        self.__decode_fn = decode_fn

    def hook(self, decode_fn: Callable[[str, ...], dict[str, any]]):
        """hook a new decode function to the decoder

        Args:
            decode_fn (Callable[[str, ...], dict[str, any]]): the decode function to hook

        Returns:
            None: nothing
        """

        self.__decode_fn = decode_fn

    def decode(self, src: str, **kwargs) -> dict[str, any]:
        """decodes a json string into a dict object using the provided decode function

        Args:
            src (str): the json string to decode
            **kwargs: any additional arguments to be passed to the decode function

        Returns:
            dict[str, any]: the decoded json object
        """

        return self.__decode_fn(src, **kwargs)


class JSONEncoder:
    """the base class for sushitools json encoders"""

    def __init__(self, encode_fn: Callable[[dict[str, any], ...], str]):
        self.__encode_fn = encode_fn

    def hook(self, encode_fn: Callable[[dict[str, any], ...], str]):
        """hook a new encode function to the encoder

        Args:
            encode_fn (Callable[[dict[str, any], ...], str]): the decode function to hook

        Returns:
            None: nothing
        """

        self.__encode_fn = encode_fn

    def encode(self, src: dict[str, any], **kwargs) -> str:
        """decodes a dict object into a json string using the provided encode function

        Args:
            src (dict[str, any]): the json object to be encoded
            **kwargs: any additional arguments to be passed to the encode function

        Returns:
            str: the encoded json string
        """

        return self.__encode_fn(src, **kwargs)


__DEFAULT_DECODER: JSONDecoder = JSONDecoder(json.loads)
__DEFAULT_ENCODER: JSONEncoder = JSONEncoder(json.dumps)


# @property  - how?
def default_decoder() -> JSONDecoder:
    """getter for the default json decoder. hooking on this object could affect your whole project

    Returns:
        JSONDecoder: the default json decoder class instance
    """

    return __DEFAULT_DECODER


# @property  - how?
def default_encoder() -> JSONEncoder:
    """getter for the default json encoder. hooking on this object could affect your whole project

    Returns:
        JSONEncoder: the default json encoder class instance
    """

    return __DEFAULT_ENCODER


def parse_json(
    src: str, decode_fn: Callable[[str, ...], dict[str, any]] = None, **kwargs
) -> dict[str, any]:
    """parses the given json string into a dict object. if the decode function is not specified, it will make use of
    the default decoder's `decode` function

    Args:
        src (str): the json source string to be parsed
        decode_fn (Callable[[str, ...], dict[str, any]]): the function used for decoding. if `None` it will fall back
        to the default decoder
        **kwargs: any additional arguments to be passed to the decode function

    Returns:
        dict[str, any]: the resulting dict object
    """

    if decode_fn:
        return decode_fn(src, **kwargs)
    else:
        return default_decoder().decode(src, **kwargs)


def to_json(
    src: dict[str, any],
    encode_fn: Callable[[dict[str, any], ...], str] = None,
    **kwargs
) -> str:
    """encodes the given dict object into a json string. if the encode function is not specified, it will make use of
    the default encoder's `encode` function

    Args:
        src (dict[str, any]): the dict object to be encoded
        encode_fn (Callable[[dict[str, any], ...], str]): the function used for encoding. if `None` it will fall back
        to the default encoder
        **kwargs: any additional arguments to be passed to the decode function

    Returns:
        str: the resulting json string
    """

    if encode_fn:
        return encode_fn(src, **kwargs)
    else:
        return default_encoder().encode(src, **kwargs)
