"""Linting methods."""

import contextlib
import copy
import io
import logging
import pathlib
import sys
import tempfile
import typing

import bandit.cli.main
import flake8.main.application
import toml

from ni_python_styleguide import _config_constants, _Flake8Error, _utils

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def lint(qs_or_vs, exclude, app_import_names, format, extend_ignore, file_or_dir):
    """Run the linter."""
    app = flake8.main.application.Application()
    args = [
        qs_or_vs,
        f"--config={_config_constants.FLAKE8_CONFIG_FILE.resolve()}",
        f"--exclude={exclude}" if exclude else "",
        f"--format={format}" if format else "",
        f"--extend-ignore={extend_ignore}" if extend_ignore else "",
        # The only way to configure flake8-black's line length is through a pyproject.toml's
        # [tool.black] setting (which makes sense if you think about it)
        # So we need to give it one
        f"--black-config={_config_constants.BLACK_CONFIG_FILE.resolve()}",
        f"--application-import-names={app_import_names}",
        *[str(p) for p in file_or_dir],
    ]
    app.run(list(filter(bool, args)))
    if app.exit_code() != 0:
        raise _Flake8Error(app.exit_code())


# Note: tried to use functools.wraps
#  - but VSCode did not properly identify the wrapped method's signature :(
def get_lint_output(qs_or_vs, exclude, app_import_names, format, extend_ignore, file_or_dir) -> str:
    "Return the output from running the linter."
    capture = io.TextIOWrapper(io.BytesIO())
    with contextlib.redirect_stdout(capture):
        try:
            lint(qs_or_vs, exclude, app_import_names, format, extend_ignore, file_or_dir)
        except _Flake8Error:
            pass
    capture.seek(0)
    return capture.read()


@contextlib.contextmanager
def _temp_sys_argv(args):
    old = sys.argv
    sys.argv = list(args)
    try:
        yield
    finally:
        sys.argv = old


@contextlib.contextmanager
def _temp_merged_config(base_config: dict, override_config_file: pathlib.Path):
    with _utils.temp_file.multi_access_tempfile(suffix=".toml") as temp:
        target = copy.deepcopy(base_config)
        merged = {"tool": {"bandit": target}}
        override_config = toml.load(override_config_file)["tool"]["bandit"]
        for key, value in override_config.items():
            if key in target and isinstance(value, list):
                _logger.debug("Merging %s: %s", key, value)
                target[key].extend(value)
            elif key in target and isinstance(value, dict):
                _logger.debug("Merging %s: %s", key, value)
                target[key].update(value)
            else:
                _logger.debug("Overriding %s: %s", key, value)
                target[key] = value
        _logger.debug("Merged config: %s", merged)

        with temp.open("w") as fout:
            toml.dump(merged, fout)

        yield temp


def _relative_to_cwd(path: str) -> pathlib.Path:
    try:
        return (pathlib.Path(path)).relative_to(pathlib.Path.cwd())
    except ValueError:
        return path


def lint_bandit(qs_or_vs, file_or_dir: typing.Tuple[pathlib.Path], pyproject_config: dict):
    """Run the bandit linter."""
    with _temp_merged_config(
        pyproject_config, _config_constants.BANDIT_CONFIG_FILE
    ) as merged_config:
        args_list = list(
            filter(
                None,
                [
                    "bandit",
                    qs_or_vs,
                    "-c",
                    str(merged_config),
                    "-r",
                    *[str(_relative_to_cwd(p)) for p in file_or_dir],
                ],
            )
        )
        _logger.debug("Running bandit with args: %s", args_list)
        with _temp_sys_argv(args_list):
            # return
            bandit.cli.main.main()
