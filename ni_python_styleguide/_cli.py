import pathlib
import sys

import click
import toml

from ni_python_styleguide import _acknowledge_existing_errors
from ni_python_styleguide import _fix
from ni_python_styleguide import _Flake8Error
from ni_python_styleguide import _lint


def _qs_or_vs(verbosity):
    if verbosity != 0:
        return f"-{'v' * verbosity if verbosity > 0 else 'q' * abs(verbosity)}"
    return ""


def _read_pyproject_toml(ctx, param, value):
    value = value or "pyproject.toml"  # Only accept local pyproject.toml if not specified

    try:
        pyproject_data = toml.load(value)
    except FileNotFoundError:
        return None
    except (toml.TomlDecodeError, OSError) as e:
        raise click.FileError(filename=value, hint=f"Error reading configuration file: {e}")

    ctx.ensure_object(dict)
    ctx.obj["PYPROJECT"] = pyproject_data
    config = pyproject_data.get("tool", {}).get("ni-python-styleguide", {})

    config.pop("quiet", None)
    config.pop("verbose", None)

    if ctx.default_map is None:
        ctx.default_map = {}
    ctx.default_map.update(config)
    return value


def _get_application_import_names(pyproject):
    """Returns the application package name the config."""
    # Otherwise override with what was specified
    app_name = (
        pyproject.get("tool", {})
        .get("ni-python-styleguide", {})
        .get("application-import-names", "")
    )

    # Allow the poetry name as a fallback
    if not app_name:
        app_name = pyproject.get("tool", {}).get("poetry", {}).get("name", "").replace("-", "_")

    return f"{app_name},tests"


class ConfigGroup(click.Group):
    """click.Group subclass which allows for a config option to load options from."""

    def __init__(self, *args, **kwargs):
        """Constructs the click.Group with the config option."""
        kwargs["params"].append(
            click.Option(
                ["--config"],
                type=click.Path(
                    exists=True,
                    file_okay=True,
                    dir_okay=False,
                    readable=True,
                    allow_dash=False,
                    path_type=str,
                ),
                is_eager=True,
                callback=_read_pyproject_toml,
                help="Config file to load configurable options from",
            )
        )

        super().__init__(*args, **kwargs)


@click.group(cls=ConfigGroup)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Print more information. Repeat to increase verbosity.",
)
@click.option(
    "-q",
    "--quiet",
    count=True,
    help="Print less information. Repeat to decrease verbosity.",
)
@click.option(
    "--exclude",
    type=str,
    show_default=True,
    default="__pycache__,.git,.venv",
    help="Comma-separated list of files or directories to exclude.",
)
@click.option(
    "--extend-exclude",
    type=str,
    default="",
    help="Comma-separated list of files or directories to exclude (in addition to --exclude).",
)
@click.version_option()  # @TODO: override the message to include dependency version(s)
@click.pass_context
def main(ctx, verbose, quiet, config, exclude, extend_exclude):
    """NI's internal and external Python linter rules and plugins."""  # noqa: D4
    ctx.ensure_object(dict)
    ctx.obj["VERBOSITY"] = verbose - quiet
    ctx.obj["EXCLUDE"] = ",".join(filter(bool, [exclude.strip(","), extend_exclude.strip(",")]))
    ctx.obj["APP_IMPORT_NAMES"] = _get_application_import_names(ctx.obj.get("PYPROJECT", {}))


@main.command()
# @TODO: When we're ready to encourage editor integration, add --diff flag
@click.option("--format", type=str, help="Format errors according to the chosen formatter.")
@click.option(
    "--extend-ignore",
    type=str,
    help="Comma-separated list of errors and warnings to ignore (or skip)",
)
@click.argument("file_or_dir", nargs=-1)
@click.pass_obj
def lint(obj, format, extend_ignore, file_or_dir):
    """Lint the file(s)/directory(s) given."""  # noqa: D4
    try:
        _lint.lint(
            qs_or_vs=_qs_or_vs(obj["VERBOSITY"]),
            exclude=obj["EXCLUDE"],
            app_import_names=obj["APP_IMPORT_NAMES"],
            format=format,
            extend_ignore=extend_ignore,
            file_or_dir=file_or_dir,
        )
    except _Flake8Error:
        sys.exit(-1)  # exit without additional output


@main.command()
@click.option(
    "--extend-ignore",
    type=str,
    help="Comma-separated list of errors and warnings to ignore (or skip)",
)
@click.argument("file_or_dir", nargs=-1)
@click.option(
    "--aggressive",
    is_flag=True,
    help="Attempt to handle long acknowledgement lines by formatting and repeating the acknowledgement.",
)
@click.pass_obj
def acknowledge_existing_violations(obj, extend_ignore, file_or_dir, aggressive):
    """Lint existing violations and acknowledge.

    Use this command to acknowledge violations in existing code to allow for enforcing new code.
    """
    _acknowledge_existing_errors.acknowledge_lint_errors(
        exclude=obj["EXCLUDE"],
        app_import_names=obj["APP_IMPORT_NAMES"],
        extend_ignore=extend_ignore,
        file_or_dir=file_or_dir,
        aggressive=aggressive,
    )


@main.command()
@click.option(
    "--extend-ignore",
    type=str,
    help="Comma-separated list of errors and warnings to ignore (or skip)",
)
@click.argument("file_or_dir", nargs=-1)
@click.option(
    "--aggressive",
    is_flag=True,
    help="Remove any existing acknowledgments, fix what can be fixed, and re-acknowledge remaining.",
)
@click.pass_obj
def fix(obj, extend_ignore, file_or_dir, aggressive):
    """Fix basic linter/formatting errors in file(s)/directory(s) given."""  # noqa: D4
    _fix.fix(
        exclude=obj["EXCLUDE"],
        app_import_names=obj["APP_IMPORT_NAMES"],
        extend_ignore=extend_ignore,
        file_or_dir=file_or_dir or [pathlib.Path.cwd()],
        aggressive=aggressive,
    )
