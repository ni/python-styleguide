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
def force_ascii_encoding(monkeypatch):
    """Force ASCII encoding as default for all file operations to catch missing encoding args."""
    import locale
    
    # Patch locale.getpreferredencoding to return 'ascii'
    # This affects Path.read_text() and Path.write_text() default encoding
    monkeypatch.setattr(locale, 'getpreferredencoding', lambda do_setlocale=True: 'ascii')
    
    # Patch builtins.open to use ASCII when encoding not specified
    original_open = builtins.open
    
    def ascii_open(*args, **kwargs):
        if 'encoding' not in kwargs:
            mode = args[1] if len(args) > 1 else kwargs.get('mode', 'r')
            if 'b' not in mode:
                kwargs['encoding'] = 'ascii'
        return original_open(*args, **kwargs)
    
    monkeypatch.setattr(builtins, 'open', ascii_open)
    
    # Patch pathlib.Path.read_text and write_text to use ASCII when encoding not specified
    original_read_text = pathlib.Path.read_text
    original_write_text = pathlib.Path.write_text
    
    def ascii_read_text(self, encoding=None, errors=None):
        if encoding is None:
            encoding = 'ascii'
        return original_read_text(self, encoding=encoding, errors=errors)
    
    def ascii_write_text(self, data, encoding=None, errors=None, newline=None):
        if encoding is None:
            encoding = 'ascii'
        return original_write_text(self, data, encoding=encoding, errors=errors, newline=newline)
    
    monkeypatch.setattr(pathlib.Path, 'read_text', ascii_read_text)
    monkeypatch.setattr(pathlib.Path, 'write_text', ascii_write_text)

    yield None