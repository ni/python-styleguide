import os

import click.testing

import pytest

from ni_python_styleguide.__main__ import main as styleguide_main


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.filterwarnings("ignore::DeprecationWarning"))


@pytest.fixture
def styleguide(monkeypatch, cli_runner):
    """A fixture which when executed, runs the styleguide.

    Args passed to the function are equivalent to CLI args,
    and are automatically stringified.

    The return value is a Result object which has an output variable and can be converted to a bool
    representing success or failure.

    E.g. `styleguide("lint", ".")`
    """

    # Add a __bool__ method so clients can assert the result
    monkeypatch.setattr(
        click.testing.Result, "__bool__", lambda s: s.exception is None, raising=False
    )

    def runner(*args):
        return cli_runner.invoke(styleguide_main, list(map(str, args)))

    return runner


@pytest.fixture
def chdir():
    cwd = os.getcwd()
    yield os.chdir
    os.chdir(cwd)
