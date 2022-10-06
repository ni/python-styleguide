"""Linting methods."""
import contextlib
from io import StringIO

import black

from ni_python_styleguide import _config_constants


def format(file_or_dir, *additional_formatter_args):
    """Format the specified file or directory using the builtin config."""
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


def format_check(file_or_dir):
    """Perform format and return True if changes were made (False otherwise)."""
    capture = StringIO()
    with contextlib.redirect_stderr(capture):
        format(file_or_dir)
    output = capture.getvalue()
    made_changes = any(["file reformatted" in output, "files reformatted" in output])

    return made_changes
