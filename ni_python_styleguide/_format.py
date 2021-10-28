"""Linting methods."""
import black

from ni_python_styleguide import _config_constants


def format(file_or_dir):
    """"Format the specified file or directory using the builtin config."""
    black.main(
        [
            *file_or_dir,
            f"--config={_config_constants.BLACK_CONFIG_FILE.resolve()}",
        ]
    )
