"""Useful plugins/fixtures which can (and should) be used in any test."""

import builtins
import functools
import io
import os
import pathlib

import click.testing
import pytest

from ni_python_styleguide.__main__ import main as styleguide_main


def pytest_collection_modifyitems(items):
    """Ignores deprecation warnings in all tests."""
    for item in items:
        item.add_marker(pytest.mark.filterwarnings("ignore::DeprecationWarning"))


@pytest.fixture
def styleguide(monkeypatch, cli_runner):
    """Runs the styleguide when executed.

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
    """Changes the current working directory when executed."""
    cwd = os.getcwd()
    yield os.chdir
    os.chdir(cwd)

@pytest.fixture(autouse=True)
def fake_open(mocker):
    """Mock open to prevent actual file system writes during tests."""
    original_open = builtins.open
    # original_path_write = pathlib.Path.write_text

    def open_with_default_ascii(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > 1:
                mode = args[1]
            else:
                mode = kwargs.get('mode', 'r')
            if 'b' not in mode and 'encoding' not in kwargs:
                kwargs['encoding'] = 'ascii'
            return func(*args, **kwargs)

        return wrapper

    original_io_open = io.open

    def io_open_with_default_encoding(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # check for encoding in args
            # self, mode, buffering, encoding, errors, newline
            mode = kwargs.get('mode', 'r')
            if len(args) > 1:
                mode = args[1]

            if len(args) > 3:
                encoding = args[3]
                args = list(args[:3])
                for name, value in zip(['errors', 'newline'], args[4:]):
                    kwargs[name] = value
            if 'encoding' not in kwargs and 'b' not in mode:
                kwargs['encoding'] = 'ascii'
            return func(*args, **kwargs)

        return wrapper

    _mock_open = mocker.patch("builtins.open", side_effect=open_with_default_ascii(original_open))
    _mock_path_write = mocker.patch("io.open", side_effect=io_open_with_default_encoding(original_io_open))
    yield None
