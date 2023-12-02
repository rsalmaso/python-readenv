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

import sys
from typing import Tuple

VersionType = Tuple[int, int, int, str, int]

PY39 = sys.version_info >= (3, 9)


def get_version(version: VersionType) -> str:
    """Returns a PEP 386-compliant version number from VERSION."""
    assert len(version) == 5
    assert version[3] in ("alpha", "beta", "rc", "final")

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts: int = 2 if version[2] == 0 else 3
    main: str = ".".join(str(x) for x in version[:parts])

    sub: str = ""

    if version[3] != "final":
        pre: str = {"alpha": "a", "beta": "b", "rc": "c"}[version[3]]
        sub = f"{pre}{version[4]}"

    return f"{main}{sub}"
