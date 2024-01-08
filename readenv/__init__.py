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

import builtins
from typing import Final

from ._environ import Environ, environ  # noqa: F401
from ._version import get_version, VersionType

bool = environ.bool
bytes = environ.bytes
decimal = environ.decimal
dict = environ.dict
float = environ.float
int = environ.int
json = environ.json
list = environ.list
tuple = environ.tuple
str = environ.str
load = environ.load
get = environ.get
set = environ.set
setdefault = environ.setdefault


VERSION: Final[VersionType] = (0, 5, 0, "final", 0)

__author__: Final[builtins.str] = "Raffaele Salmaso"
__author_email__: Final[builtins.str] = "raffaele.salmaso@gmail.com"
__version__: Final[builtins.str] = get_version(VERSION)
