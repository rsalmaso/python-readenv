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
import os
import pathlib
import re
from typing import (
    Any,
    Callable,
    cast as typing_cast,
    Dict,
    Final,
    List,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

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


PatternType = Pattern[str]
MatchType = Match[str]
CastCallable = Callable[..., object]
OptionalCastCallable = Union[CastCallable, Undefined]
T = TypeVar("T", bound=Any)

undefined: Final[Undefined] = Undefined()
_RE1: Final[PatternType] = re.compile(r"\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z")
_RE2: Final[PatternType] = re.compile(r"\A'(.*)'\Z")
_posix_variable: Final[PatternType] = re.compile(r"\$\{[^\}]*\}")


def _cast_bool(value: str) -> bool:
    try:
        return int(value) != 0
    except ValueError:
        value = value.lower()
        if value in ("y", "yes", "t", "true"):
            return True
        elif value in ("n", "no", "f", "false"):
            return False
    raise ValueError("not a boolean value")


def _cast_list(value: str) -> List[str]:
    return [x for x in value.split(",") if x]


def _cast_tuple(value: str) -> Tuple[str, ...]:
    return tuple([x for x in value.split(",") if x])


def _cast_dict(value: str) -> Dict[str, Any]:
    return dict([val.split("=") for val in value.split(",") if val])


def _cast_json(value: str) -> Any:
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
        else:
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

    def _load(self, filename: Union[str, pathlib.PurePath]) -> None:
        path: pathlib.Path = pathlib.Path(filename)
        content: str = self._get_content(path) if path.is_absolute() else self._get_content_from_parts(str(filename))

        for line in content.splitlines():  # ???
            m1: Optional[MatchType] = _RE1.match(line)
            key: str
            val: str
            if m1:
                key, val = m1.group(1), m1.group(2)
                m2: Optional[MatchType] = _RE2.match(val)
                if m2:
                    val = m2.group(1)
                m3: Optional[MatchType] = _RE2.match(val)
                if m3:
                    val = re.sub(r"\\(.)", r"\1", m3.group(1))
                # expand values
                val = _posix_variable.sub(self._replace, val)
                self.set(key, val)  # override if exists

    def load(self, *filenames: Union[str, pathlib.PurePath]) -> None:
        """Load a list of filename.env [default=(".env", ".env.local")]"""
        filenames = filenames if filenames else (".env", ".env.local")
        for filename in filenames:
            self._load(filename)

    _bool: TypeAlias = bool

    def bool(self, key: str, default: Union[bool, Undefined] = undefined) -> bool:
        return self.get(key, default=default, cast=_cast_bool)

    def bytes(self, key: str, default: Union[bytes, Undefined] = undefined) -> bytes:
        return self.get(key, default=default, cast=bytes)

    def decimal(self, key: str, default: Union[Decimal, Undefined] = undefined) -> Decimal:
        return self.get(key, default=default, cast=Decimal)

    def dict(self, key: str, default: Union[Dict[str, Any], Undefined] = undefined) -> Dict[str, Any]:
        return self.get(key, default=default, cast=_cast_dict)

    def float(self, key: str, default: Union[float, Undefined] = undefined) -> float:
        return self.get(key, default=default, cast=float)

    def int(self, key: str, default: Union[int, Undefined] = undefined) -> int:
        return self.get(key, default=default, cast=int)

    def json(self, key: str, default: Union[Any, Undefined] = undefined) -> Any:
        return self.get(key, default=default, cast=_cast_json)

    def list(self, key: str, default: Union[List[str], Undefined] = undefined) -> List[str]:
        return self.get(key, default=default, cast=_cast_list)

    def tuple(self, key: str, default: Union[Tuple[str], Undefined] = undefined) -> Tuple[str]:
        return self.get(key, default=default, cast=_cast_tuple)

    def str(self, key: str, default: Union[str, Undefined] = undefined, *, multiline: _bool = False) -> str:
        value: str = self.get(key, default)
        if multiline:
            return value.replace("\\n", "\n")
        return value


environ = Environ(os.environ)
