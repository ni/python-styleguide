"""Linting methods."""
from io import StringIO
import contextlib

import black

from ni_python_styleguide import _config_constants


def format(file_or_dir, *additional_formatter_args):
    """"Format the specified file or directory using the builtin config."""
    try:
        black.main(
            [
                str(file_or_dir),
                f"--config={_config_constants.BLACK_CONFIG_FILE.resolve()}",
                *additional_formatter_args,
            ]
        )
    except SystemExit as e:
        if e.code == 0:
            pass  # why are they exiting when called via import ?! ‾\_(ツ)_/‾
        else:
            raise


def does_formatting_make_changes(file_or_dir):
    capture = StringIO()
    with contextlib.redirect_stderr(capture):
        format(file_or_dir)
    output = capture.getvalue()
    made_changes = any(["file reformatted" in output, "files reformatted" in output])

    return made_changes
