import os
from typing import Final, List

import nox

FILES: Final[List[str]] = ["readenv", "noxfile.py"]
PYTHON: Final[List[str]] = ["3.8", "3.9", "3.10", "3.11", "3.12"]

nox.options.sessions = ["lint"]


def requirements_file(session: nox.Session) -> str:
    return f"requirements-{session.python}.txt"


def install(session: nox.Session) -> None:
    with session.cd("requirements"):
        session.install("-r", requirements_file(session))


@nox.session(python=["3.10"])
def lint(session: nox.Session) -> None:
    install(session)
    session.run("ruff", *FILES)
    session.run("mypy", *FILES)


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
