import logging
import pathlib
from collections import defaultdict
from fnmatch import fnmatch
from typing import Iterable

import isort

from ni_python_styleguide import _acknowledge_existing_errors
from ni_python_styleguide import _config_constants
from ni_python_styleguide import _format
from ni_python_styleguide import _utils

_module_logger = logging.getLogger(__name__)


def _split_imports_line(lines: str, *_, **__):
    r"""Splits multi-import lines to multiple lines.

    >>> _split_imports_line("import os, collections\n")
    'import os\nimport collections\n'

    >>> _split_imports_line("import os\n")
    'import os\n'

    >>> _split_imports_line("from ni_python_styleguide import"
    ... " _acknowledge_existing_errors, _format")
    'from ni_python_styleguide import _acknowledge_existing_errors\nfrom ni_python_styleguide import _format\n'

    >>> _split_imports_line("from ni_python_styleguide import _acknowledge_existing_errors")
    'from ni_python_styleguide import _acknowledge_existing_errors\n'

    >>> _split_imports_line("import os, collections\nimport pathlib")
    'import os\nimport collections\nimport pathlib\n'

    >>> _split_imports_line("import os, collections\nimport pathlib, os")
    'import os\nimport collections\nimport pathlib\nimport os\n'

    >>> _split_imports_line("\n")
    '\n'
    """  # noqa W505: long lines...
    result_parts = []
    for line in lines.splitlines(keepends=True):
        code_portion_of_line, *non_code = line.split("#", maxsplit=1)
        first, _, rest = code_portion_of_line.partition(",")
        if not all(
            [
                rest,
                "import " in code_portion_of_line,
                code_portion_of_line.strip().startswith("import ")
                or code_portion_of_line.strip().startswith("from "),
            ]
        ):
            result_parts.append(code_portion_of_line)
            continue
        prefix, first = " ".join(first.split()[:-1]), first.split()[-1]
        split_up = [first] + rest.split(",")
        result_parts.extend([prefix + " " + part.strip() for part in split_up])
    suffix = ""
    if non_code:
        suffix = "#" + "".join(non_code)
    result = "\n".join(result_parts) + suffix
    if result.strip():
        return result.rstrip() + "\n"
    return result


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
    _format.format(file)


def fix(
    exclude: str,
    app_import_names: str,
    extend_ignore,
    file_or_dir,
    *_,
    aggressive=False,
):
    """Fix basic linter errors and format."""
    file_or_dir = file_or_dir or ["."]
    if aggressive:
        all_files = []
        for file_or_dir_ in file_or_dir:
            file_path = pathlib.Path(file_or_dir_)
            if file_path.is_dir():
                all_files.extend(file_path.rglob("*.py"))
            else:
                all_files.append(file_path)
        all_files = filter(
            lambda o: not any([fnmatch(o, exclude_) for exclude_ in exclude.split(",")]), all_files
        )
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
    for bad_file, errors_in_file in lint_errors_by_file.items():
        try:
            _format.format(bad_file)
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
        except Exception as e:
            failed_files.append((bad_file, e))
    if failed_files:
        raise Exception(
            "Failed to format files:\n"
            + "\n".join([f"{file}: {error}" for file, error in failed_files])
        )
