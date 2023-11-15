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

import os
from typing import Any, Callable, cast as typing_cast, Final, TypeVar, Union

__all__ = ["get", "set", "setdefault"]


class Undefined:
    pass


undefined: Final[Undefined] = Undefined()


T = TypeVar("T", bound=Any)

CastCallable = Callable[..., object]
OptionalCastCallable = Union[CastCallable, Undefined]


def get(key: str, default: Union[T, Undefined] = undefined, *, cast: OptionalCastCallable = undefined) -> T:
    value: Any
    try:
        value = os.environ[key]
    except KeyError:
        if isinstance(default, Undefined):
            raise KeyError(f"Cannot find {key} in the environment")
        value = default
    else:
        if callable(cast):
            value = cast(value)
    return typing_cast(T, value)


def set(key: str, value: Any) -> None:
    os.environ[key] = str(value)


def setdefault(key: str, value: Any) -> None:
    os.environ.setdefault(key, str(value))
