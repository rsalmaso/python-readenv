import os
from typing import Final, List

import nox

PYTHON: Final[List[str]] = ["3.8", "3.9", "3.10", "3.11", "3.12"]


def requirements_file(session: nox.Session) -> str:
    return f"requirements-{session.python}.txt"


@nox.session(python=PYTHON)
def requirements(session: nox.Session) -> None:
    with session.cd("requirements"):
        session.install("pip-tools")
        try:
            with open("requirements.in", "wt") as fout:
                with open("../requirements.in", "rt") as fin:
                    fout.write(fin.read())
                    fout.flush()
                session.run(
                    "pip-compile",
                    "--upgrade",
                    "--annotation-style=line",
                    f"--output-file={requirements_file(session)}",
                    "requirements.in",
                )
        finally:
            os.unlink("requirements.in")
