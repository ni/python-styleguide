import logging
import pathlib
from collections import defaultdict
from typing import Iterable

import better_diff.unified_plus
import isort
import pathspec

from ni_python_styleguide import (
    _acknowledge_existing_errors,
    _config_constants,
    _format,
    _utils,
)
from ni_python_styleguide._utils import temp_file

_module_logger = logging.getLogger(__name__)
_module_logger.addHandler(logging.NullHandler())


def _sort_imports(file: pathlib.Path, app_import_names):
    raw = file.read_text()
    isort_config = isort.Config(
        settings_file=str(_config_constants.ISORT_CONFIG_FILE),
        known_first_party=filter(None, app_import_names.split(",")),
    )
    output = isort.code(
        raw,
        config=isort_config,
    )
    file.write_text(output)


def _format_imports(file: pathlib.Path, app_import_names: Iterable[str]) -> None:
    _sort_imports(file, app_import_names=app_import_names)
    _format.format(file, "-q")


def _posix_relative_if_under(file: pathlib.Path, base: pathlib.Path) -> str:
    file_resolved = file.resolve()
    base_resolved = base.resolve()
    if file_resolved.as_posix().startswith(base_resolved.as_posix()):
        return file_resolved.relative_to(base_resolved).as_posix()
    return file_resolved.as_posix()


def fix(
    exclude: str,
    app_import_names: str,
    extend_ignore,
    file_or_dir,
    *_,
    aggressive=False,
    diff=False,
    check=False,
):
    """Fix basic linter errors and format."""
    file_or_dir = file_or_dir or ["."]
    if diff or check:
        if aggressive:
            raise Exception("Cannot use --aggressive with --diff or --check")
    if aggressive:
        glob_spec = pathspec.PathSpec.from_lines(
            "gitwildmatch",
            ["*.py"]
            + [f"!{exclude_}" for exclude_ in exclude.split(",") if exclude_]
            + [f"!{ignore_}" for ignore_ in extend_ignore.split(",") if ignore_],
        )
        all_files = []
        for file_or_dir_ in file_or_dir:
            file_path = pathlib.Path(file_or_dir_)
            if file_path.is_dir():
                all_files.extend(
                    [pathlib.Path(o) for o in glob_spec.match_tree(str(file_path), negate=False)]
                )
            else:
                all_files.append(file_path)
        for file in all_files:
            if not file.is_file():  # doesn't really exist...
                continue
            _acknowledge_existing_errors.remove_auto_suppressions_from_file(file)
    lint_errors_to_process = _acknowledge_existing_errors._utils.lint.get_errors_to_process(
        exclude,
        app_import_names,
        extend_ignore,
        [pathlib.Path(file_or_dir_) for file_or_dir_ in file_or_dir],
        excluded_errors=[],  # we fix black errors, so we don't need to filter it.
    )

    lint_errors_by_file = defaultdict(list)
    for error in lint_errors_to_process:
        lint_errors_by_file[pathlib.Path(error.file)].append(error)

    failed_files = []
    make_changes = not (diff or check)
    for bad_file, errors_in_file in lint_errors_by_file.items():
        try:
            if make_changes:
                _format.format(bad_file, "-q")
                _format_imports(file=bad_file, app_import_names=app_import_names)
                remaining_lint_errors_in_file = _utils.lint.get_errors_to_process(
                    exclude,
                    app_import_names,
                    extend_ignore,
                    [bad_file],
                    excluded_errors=[],
                )
                if remaining_lint_errors_in_file and aggressive:
                    _acknowledge_existing_errors.acknowledge_lint_errors(
                        exclude=exclude,
                        app_import_names=app_import_names,
                        extend_ignore=extend_ignore,
                        aggressive=aggressive,
                        file_or_dir=[bad_file],
                    )
            else:
                with temp_file.multi_access_tempfile(suffix="__" + bad_file.name) as working_file:
                    working_file.write_text(bad_file.read_text())
                    _format.format(working_file, "-q")
                    _format_imports(file=working_file, app_import_names=app_import_names)

                    diff_lines = better_diff.unified_plus.format_diff(
                        bad_file.read_text(),
                        working_file.read_text(),
                        tofile=f"{_posix_relative_if_under(bad_file, pathlib.Path.cwd())}_formatted",
                    )
                    if diff:
                        print(diff_lines)
                    if check and diff_lines:
                        print("Error: file would be changed:", str(bad_file))
                        failed_files.append((bad_file, "File would be changed."))

        except Exception as e:
            failed_files.append((bad_file, e))
    if failed_files:
        raise Exception(
            "Failed to format files:\n"
            + "\n".join([f"{file}: {error}" for file, error in failed_files])
        )
