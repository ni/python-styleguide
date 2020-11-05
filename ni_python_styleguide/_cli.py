import pathlib

import click

import flake8.main.application

import toml


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

    config = pyproject_data.get("tool", {}).get("ni-python-styleguide", {})

    config.pop("quiet", None)
    config.pop("verbose", None)

    if ctx.default_map is None:
        ctx.default_map = {}
    ctx.default_map.update(config)
    return value


class AllowConfigGroup(click.Group):
    def __init__(self, *args, **kwargs):

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


@click.group(cls=AllowConfigGroup)
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
    ctx.ensure_object(dict)
    ctx.obj["VERBOSITY"] = verbose - quiet
    ctx.obj["EXCLUDE"] = ",".join(filter(bool, [exclude.strip(","), extend_exclude.strip(",")]))


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
    app = flake8.main.application.Application()
    args = [
        _qs_or_vs(obj["VERBOSITY"]),
        f"--config={(pathlib.Path(__file__).parent / 'config.ini').resolve()}",
        f"--exclude={obj['EXCLUDE']}" if obj["EXCLUDE"] else "",
        f"--format={format}" if format else "",
        f"--extend-ignore={extend_ignore}" if extend_ignore else "",
        # The only way to configure flake8-black's line length is through a pyproject.toml's
        # [tool.black] setting (which makes sense if you think about it)
        # So we need to give it one
        f"--black-config={(pathlib.Path(__file__).parent / 'config.toml').resolve()}",
        *file_or_dir,
    ]
    app.run(list(filter(bool, args)))
    app.exit()
