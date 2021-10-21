"""Linting methods."""
import pathlib

import flake8.main.application


def lint(qs_or_vs, exclude, app_import_names, format, extend_ignore, file_or_dir):
    """Run the linter."""
    app = flake8.main.application.Application()
    args = [
        qs_or_vs,
        f"--config={(pathlib.Path(__file__).parent / 'config.ini').resolve()}",
        f"--exclude={exclude}" if exclude else "",
        f"--format={format}" if format else "",
        f"--extend-ignore={extend_ignore}" if extend_ignore else "",
        # The only way to configure flake8-black's line length is through a pyproject.toml's
        # [tool.black] setting (which makes sense if you think about it)
        # So we need to give it one
        f"--black-config={(pathlib.Path(__file__).parent / 'config.toml').resolve()}",
        f"--application-import-names={app_import_names}",
        *file_or_dir,
    ]
    app.run(list(filter(bool, args)))
    app.exit()
