import contextlib
import copy
import os
from typing import Any, Generator

import readenv


@contextlib.contextmanager
def load(envfile: str = "tests/test.env") -> Generator[Any, Any, Any]:
    environ = copy.deepcopy(os.environ)
    readenv.load(envfile)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(environ)
