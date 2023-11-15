# Copyright (C) Raffaele Salmaso <raffaele.salmaso@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from decimal import Decimal
import json
from typing import Any, Dict, List, Tuple, Union

from .env import get, Undefined, undefined


class ConverterNotAvailable(ValueError):
    pass


def to_str(key: str, default: Union[str, Undefined] = undefined, *, multiline: bool = False) -> str:
    value: str = get(key, default)
    if multiline:
        return value.replace("\\n", "\n")
    return value


def to_bytes(key: str, default: Union[bytes, Undefined] = undefined) -> bytes:
    return get(key, default=default, cast=bytes)


def _cast_bool(value: str) -> bool:
    res: bool
    try:
        res = int(value) != 0
    except ValueError:
        value = value.lower()
        if value in ("y", "yes", "t", "true"):
            res = True
        elif value in ("n", "no", "f", "false"):
            res = False
        else:
            raise ValueError("not a boolean value")
    return res


def to_bool(key: str, default: Union[bool, Undefined] = undefined) -> bool:
    return get(key, default=default, cast=_cast_bool)


def to_int(key: str, default: Union[int, Undefined] = undefined) -> int:
    return get(key, default=default, cast=int)


def to_float(key: str, default: Union[float, Undefined] = undefined) -> float:
    return get(key, default=default, cast=float)


def to_decimal(key: str, default: Union[Decimal, Undefined] = undefined) -> Decimal:
    return get(key, default=default, cast=Decimal)


def _cast_list(value: str) -> List[str]:
    return [x for x in value.split(",") if x]


def to_list(key: str, default: Union[List[str], Undefined] = undefined) -> List[str]:
    return get(key, default=default, cast=_cast_list)


def _cast_tuple(value: str) -> Tuple[str, ...]:
    return tuple([x for x in value.split(",") if x])


def to_tuple(key: str, default: Union[Tuple[str], Undefined] = undefined) -> Tuple[str]:
    return get(key, default=default, cast=_cast_tuple)


def _cast_dict(value: str) -> Dict[str, Any]:
    return dict([val.split("=") for val in value.split(",") if val])


def to_dict(key: str, default: Union[Dict[str, Any], Undefined] = undefined) -> Dict[str, Any]:
    return get(key, default=default, cast=_cast_dict)


def _cast_json(value: str) -> Any:
    return json.loads(value)


def to_json(key: str, default: Union[Any, Undefined] = undefined) -> Any:
    return get(key, default=default, cast=_cast_json)
