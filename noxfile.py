from typing import Final, List

import nox

FILES: Final[List[str]] = ["readenv", "tests", "noxfile.py"]
PYTHON: Final[List[str]] = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]

nox.options.sessions = ["lint", "tests"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True
nox.options.default_venv_backend = "uv|virtualenv"


def install(session: nox.Session) -> None:
    pyproject = nox.project.load_toml("pyproject.toml")
    session.install(
        *nox.project.dependency_groups(pyproject, "dev"),
    )


@nox.session(python=PYTHON)
def tests(session: nox.Session) -> None:
    install(session)
    session.run("pytest")


@nox.session(python=["3.10"])
def lint(session: nox.Session) -> None:
    install(session)
    session.run("ruff", "check", *FILES)
    session.run("ruff", "format", "--check", *FILES)
    session.run("mypy", *FILES)
