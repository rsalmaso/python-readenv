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
import pathlib
import re
from typing import Final, Optional, Sequence, Union

from . import env
from .version import PY39

__all__ = ["load"]

if PY39:
    from .typing39 import MatchType, PatternType
else:
    from .typing38 import MatchType, PatternType

RE1: Final[PatternType] = re.compile(r"\A(?:export )?([A-Za-z_0-9]+)=(.*)\Z")
RE2: Final[PatternType] = re.compile(r"\A'(.*)'\Z")
__posix_variable: Final[PatternType] = re.compile(r"\$\{[^\}]*\}")


def replace(match: MatchType) -> str:
    name = match.group()[2:-1]
    return env.get(name, "")


def get_content(filename: pathlib.Path) -> str:
    content: str = ""
    try:
        with open(str(filename)) as f:
            content = f.read()
    except IOError:
        pass
    return content


def get_content_from_parts(filename: str) -> str:
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


def _load(filename: Union[str, pathlib.PurePath]) -> None:
    path: pathlib.Path = pathlib.Path(filename)
    content: str = get_content(path) if path.is_absolute() else get_content_from_parts(str(filename))

    for line in content.splitlines():  # ???
        m1: Optional[MatchType] = RE1.match(line)
        key: str
        val: str
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2: Optional[MatchType] = RE2.match(val)
            if m2:
                val = m2.group(1)
            m3: Optional[MatchType] = RE2.match(val)
            if m3:
                val = re.sub(r"\\(.)", r"\1", m3.group(1))
            # expand values
            val = __posix_variable.sub(replace, val)
            env.set(key, val)  # override if exists


def load(*filenames: Union[str, pathlib.PurePath]) -> None:
    """Load a list of filename.env [default=(".env", ".env.local")]"""
    filenames = filenames if filenames else (".env", ".env.local")
    for filename in filenames:
        _load(filename)
