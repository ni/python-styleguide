import fileinput
import logging
import pathlib
from collections import defaultdict
from fnmatch import fnmatch
from typing import List

import isort

from ni_python_styleguide import _acknowledge_existing_errors
from ni_python_styleguide import _format
from ni_python_styleguide import _utils

_module_logger = logging.getLogger(__name__)


def _split_imports_line(lines: str, *_, **__):
    r"""Split multi-import lines to multiple lines.

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
    output = isort.code(
        raw,
        multi_line_output=3,
        line_length=1,
        known_first_party=filter(None, app_import_names.split(",")),
    )
    file.write_text(output)


def _handle_multiple_import_lines(bad_file: pathlib.Path):
    multiline_string_checker = _utils.string_helpers.InMultiLineStringChecker(
        lines=bad_file.read_text(encoding=_utils.DEFAULT_ENCODING).splitlines()
    )
    with fileinput.FileInput(files=[str(bad_file)], inplace=True) as f:
        for line_no, line in enumerate(f):
            working_line = line
            if multiline_string_checker.in_multiline_string(line_no + 1):
                print(working_line, end="")
                continue
            working_line = _split_imports_line(working_line)
            print(working_line, end="")


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
        errors_in_file: List[_utils.lint.LintError]
        try:
            _format.format(bad_file)
            line_to_codes_mapping = defaultdict(set)
            for error in errors_in_file:
                # humans talk 1-based, enumerate is 0-based
                line_to_codes_mapping[int(error.line) - 1].add(error.code)
            _sort_imports(bad_file, app_import_names=app_import_names)
            _format.format(bad_file, "--line-length=300")  # condense any split lines
            _handle_multiple_import_lines(bad_file)
            _format.format(bad_file)
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
                    errors_in_file=remaining_lint_errors_in_file,
                )
        except AttributeError as e:
            failed_files.append((bad_file, e))
    if failed_files:
        raise Exception(
            "Failed to format files:\n"
            + "\n".join([f"{file}: {error}" for file, error in failed_files])
        )
