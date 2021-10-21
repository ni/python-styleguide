"""Linting methods."""
import flake8.main.application

from ni_python_styleguide import _config_constants


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
        *file_or_dir,
    ]
    app.run(list(filter(bool, args)))
    app.exit()
