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

import base64
import binascii
from decimal import Decimal
import json
import os
import pathlib
import re
from typing import (
    Any,
    Callable,
    Dict,
    Final,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
from typing import cast as typing_cast

try:
    from typing import TypeAlias  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias

from ._version import PY39

if PY39:
    from re import Match, Pattern
else:
    from typing import Match, Pattern

__all__ = ["Environ"]


class Undefined:
    pass


T = TypeVar("T", bound=Any)
PatternType: TypeAlias = Pattern[str]
MatchType: TypeAlias = Match[str]
CastCallable: TypeAlias = Callable[..., Any]
OptionalCastCallable: TypeAlias = Union[CastCallable, Undefined]
_bool: TypeAlias = bool

undefined: Final[Undefined] = Undefined()
_RE1: Final[PatternType] = re.compile(r"\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z")
_RE2: Final[PatternType] = re.compile(r"\A'(.*)'\Z")
_posix_variable: Final[PatternType] = re.compile(r"\$\{[^\}]*\}")


def _cast_bool(value: Union[bool, int, str]) -> bool:
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        try:
            return bool(int(value))
        except ValueError:
            value = value.lower()
            if value in ("y", "yes", "t", "true"):
                return True
            elif value in ("n", "no", "f", "false"):
                return False
        raise ValueError("not a boolean value")
    return value


def _cast_list(
    value: Union[str, Iterable[str]],
    *,
    separator: str = ",",
    cast: OptionalCastCallable = undefined,
) -> List[str]:
    if isinstance(value, str):
        if isinstance(cast, Undefined):
            return [x for x in value.split(separator) if x]
        return [cast(x) for x in value.split(separator) if x]
    if isinstance(cast, Undefined):
        return [x for x in value if x]
    return [cast(x) for x in value if x]


def _cast_tuple(
    value: Union[str, Iterable[str]],
    *,
    separator: str = ",",
    cast: OptionalCastCallable = undefined,
) -> Tuple[str, ...]:
    return tuple(_cast_list(value, separator=separator, cast=cast))


def _cast_dict(
    value: Union[Mapping[Any, Any], str],
    *,
    separator: str = ",",
    value_separator: str = "=",
) -> Mapping[Any, Any]:
    if isinstance(value, Mapping):
        return value
    if isinstance(value, str):
        return dict([val.split(value_separator) for val in value.split(separator) if val])
    raise ValueError("not a mapping value")


def _cast_json(value: str) -> Any:
    try:
        value = base64.b64decode(value, validate=True).decode("utf-8")
    except binascii.Error:
        pass
    return json.loads(value)


class Environ:
    def __init__(self, environ: Union[Undefined, MutableMapping[str, Any]] = undefined) -> None:
        self.environ: MutableMapping[str, Any] = {} if isinstance(environ, Undefined) else environ

    def get(
        self,
        key: str,
        default: Union[T, Undefined] = undefined,
        *,
        cast: OptionalCastCallable = undefined,
    ) -> T:
        value: Any
        try:
            value = self.environ[key]
        except KeyError:
            if isinstance(default, Undefined):
                raise KeyError(f"Cannot find {key} in the environment")
            value = default
        if callable(cast):
            value = cast(value)
        return typing_cast(T, value)

    def set(self, key: str, value: Any) -> None:
        self.environ[key] = str(value)

    def setdefault(self, key: str, value: Any) -> None:
        self.environ.setdefault(key, str(value))

    def _replace(self, match: MatchType) -> str:
        name = match.group()[2:-1]
        return self.get(name, "")

    def _get_content(self, filename: pathlib.Path) -> str:
        content: str = ""
        try:
            with open(str(filename)) as f:
                content = f.read()
        except IOError:
            pass
        return content

    def _get_content_from_parts(self, filename: str) -> str:
        parts: Sequence[str] = pathlib.Path().cwd().parts
        content: str = ""
        for index in reversed(list(range(1, len(parts) + 1))):
            path: pathlib.Path = pathlib.Path(os.path.join(*parts[:index], filename))
            try:
                with open(str(path)) as f:
                    content = f.read()
                    break
            except IOError:
                pass
        return content

    def _load(self, filename: Union[str, pathlib.PurePath]) -> Mapping[str, str]:
        path: pathlib.Path = pathlib.Path(filename)
        content: str = self._get_content(path) if path.is_absolute() else self._get_content_from_parts(str(filename))
        environ: Dict[str, str] = {}

        for line in content.splitlines():  # ???
            m1: Optional[MatchType] = _RE1.match(line)
            key: str
            value: str
            if m1:
                key, value = m1.group(1), m1.group(2)
                m2: Optional[MatchType] = _RE2.match(value)
                if m2:
                    value = m2.group(1)
                m3: Optional[MatchType] = _RE2.match(value)
                if m3:
                    value = re.sub(r"\\(.)", r"\1", m3.group(1))
                # expand values
                environ[key] = _posix_variable.sub(self._replace, value)
        return environ

    def load(self, *filenames: Union[str, pathlib.PurePath]) -> None:
        """Load a list of filename.env [default=(".env", ".env.local")]"""
        filenames = filenames if filenames else (".env", ".env.local")

        # collect all vars
        environ: Dict[str, str] = {}
        for filename in filenames:
            environ.update(self._load(filename))

        # set
        for key, value in environ.items():
            self.setdefault(key, value)

    def bool(self, key: str, default: Union[bool, int, str, Undefined] = undefined) -> bool:
        return self.get(key, default=default, cast=_cast_bool)  # type: ignore[return-value]

    def bytes(self, key: str, default: Union[bytes, Undefined] = undefined) -> bytes:
        return self.get(key, default=default, cast=bytes)

    def decimal(self, key: str, default: Union[Decimal, int, str, Undefined] = undefined) -> Decimal:
        return self.get(key, default=default, cast=Decimal)  # type: ignore[return-value]

    def dict(
        self,
        key: str,
        default: Union[Mapping[Any, Any], Undefined] = undefined,
        *,
        separator: str = ",",
        value_separator: str = "=",
    ) -> Mapping[Any, Any]:
        return self.get(
            key,
            default=default,
            cast=lambda value: _cast_dict(value, separator=separator, value_separator=value_separator),
        )

    def float(self, key: str, default: Union[float, str, Undefined] = undefined) -> float:
        return self.get(key, default=default, cast=float)  # type: ignore[return-value]

    def int(self, key: str, default: Union[int, str, Undefined] = undefined) -> int:
        return self.get(key, default=default, cast=int)  # type: ignore[return-value]

    def json(self, key: str, default: Union[Any, Undefined] = undefined) -> Any:
        return self.get(key, default=default, cast=_cast_json)

    def list(
        self,
        key: str,
        default: Union[str, Iterable[str], Undefined] = undefined,
        *,
        separator: str = ",",
        cast: OptionalCastCallable = undefined,
    ) -> List[str]:
        return typing_cast(
            List[str],
            self.get(key, default=default, cast=lambda value: _cast_list(value, separator=separator, cast=cast)),
        )

    def tuple(
        self,
        key: str,
        default: Union[str, Iterable[str], Undefined] = undefined,
        *,
        separator: str = ",",
        cast: OptionalCastCallable = undefined,
    ) -> Tuple[str]:
        return typing_cast(
            Tuple[str],
            self.get(key, default=default, cast=lambda value: _cast_tuple(value, separator=separator, cast=cast)),
        )

    def str(self, key: str, default: Union[str, Undefined] = undefined, *, multiline: _bool = False) -> str:
        value: str = self.get(key, default)
        if multiline:
            return value.replace("\\n", "\n")
        return value


environ = Environ(os.environ)
