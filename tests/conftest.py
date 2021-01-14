"""Useful plugins/fixtures which can (and should) be used in any test."""

import os
import logging

import click.testing

import pytest

from ni_python_styleguide.__main__ import main as styleguide_main


def pytest_collection_modifyitems(items):
    """Ignore deprecation warnings in all tests."""
    for item in items:
        item.add_marker(pytest.mark.filterwarnings("ignore::DeprecationWarning"))


@pytest.fixture
def styleguide(monkeypatch, cli_runner):
    """Fixture which runs the styleguide when executed.

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
def styleguide_command(styleguide, chdir, tmp_path):
    """Fixture which will run the styleguide with the passed subcommand.

    Both `base_args` and `command_args` must be iterables which will be transformed into strings
    and passed on the cmd line in the following order: `<cmd> <base_args> <command> <command_args>.
    """

    def runner(*, base_args=[], command="", command_args=[]):
        return styleguide(*base_args, command, *command_args)

    chdir(str(tmp_path))

    yield runner


@pytest.fixture
def chdir():
    """Fixture which changes the current working directory when executed."""
    cwd = os.getcwd()
    yield os.chdir
    os.chdir(cwd)
