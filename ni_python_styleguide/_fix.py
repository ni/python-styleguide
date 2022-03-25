import fileinput
import logging
import pathlib
from collections import defaultdict
from typing import Iterable, List

import ni_python_styleguide._utils
from ni_python_styleguide import _acknowledge_existing_errors, _format
from ni_python_styleguide._acknowledge_existing_errors import _lint_errors_parser


_module_logger = logging.getLogger(__name__)


def _split_imports_line(lines: str, *_, **__):
    r"""Split multi-import lines to multiple lines.

    >>> _split_imports_line("import os, collections\n")
    'import os\nimport collections\n'

    >>> _split_imports_line("import os\n")
    'import os\n'

    >>> _split_imports_line("from ni_python_styleguide import"
    ... " _acknowledge_existing_errors, _format")
    'from ni_python_styleguide import _acknowledge_existing_errors\n"
    ... "from ni_python_styleguide import _format\n'

    >>> _split_imports_line("from ni_python_styleguide import _acknowledge_existing_errors")
    'from ni_python_styleguide import _acknowledge_existing_errors\n'

    >>> _split_imports_line("import os, collections\nimport pathlib")
    'import os\nimport collections\nimport pathlib\n'

    >>> _split_imports_line("import os, collections\nimport pathlib, os")
    'import os\nimport collections\nimport pathlib\nimport os\n'
    """
    result_parts = []
    for line in lines.splitlines():
        first, _, rest = line.partition(",")
        if not rest or "import" not in line:
            result_parts.append(line)
            continue
        prefix, first = " ".join(first.split()[:-1]), first.split()[-1]
        split_up = [first] + rest.split(",")
        result_parts.extend([prefix + " " + part.strip() for part in split_up])
    result = "\n".join(result_parts)
    if result:
        return result + "\n"
    return result


def _split_imports(file: pathlib.Path, offending_lines: Iterable[int]):
    _module_logger("Splitting import lines in file: %s", file)
    hashed_offending_lines = set(offending_lines)
    with fileinput.input(file, inplace=True) as py_file:
        for line_no, line in py_file:
            if line_no in hashed_offending_lines:
                print(_split_imports_line(line))
            else:
                print(line)


def _sort_imports():
    pass


def _remove_unused_non_fist_party_imports(lines: str, *_, **__):
    return lines


CODE_TO_HANDLER_MAPPING = {
    "I100": _sort_imports,
    "I201": _sort_imports,
    "F401": _remove_unused_non_fist_party_imports,
    "E401": _split_imports,
}


def fix(exclude, app_import_names, extend_ignore, file_or_dir, *_, aggressive=False, diff=False):
    """Fix basic linter errors and format."""
    if aggressive:
        raise Exception("--aggressive is not implemented yet")
    lint_errors_to_process = _acknowledge_existing_errors._get_lint_errors_to_process(
        exclude,
        app_import_names,
        extend_ignore,
        [pathlib.Path(file_or_dir_) for file_or_dir_ in file_or_dir or "."],
        excluded_errors=[],  # we fix black errors, so we don't need to filter it.
    )

    lint_errors_by_file = defaultdict(list)
    for error in lint_errors_to_process:
        lint_errors_by_file[pathlib.Path(error.file)].append(error)

    failed_files = []
    for bad_file, errors_in_file in lint_errors_by_file.items():
        errors_in_file: List[_lint_errors_parser.LintError]
        try:
            _format.format(bad_file)
            line_to_codes_mapping = defaultdict(set)
            for error in errors_in_file:
                # humans talk 1-based, enumerate is 0-based
                line_to_codes_mapping[int(error.line) - 1].add(error.code)
            # in_memory_file = deque(bad_file.read_text().splitlines())
            with fileinput.FileInput(files=[str(bad_file)], inplace=True) as f:
                for line_no, line in enumerate(f):
                    if not any(
                        [
                            line_no in line_to_codes_mapping,
                            any(
                                [
                                    code in CODE_TO_HANDLER_MAPPING
                                    for code in line_to_codes_mapping.get(line_no, [])
                                ]
                            ),
                        ]
                    ):
                        print(line, end="")
                        continue

                    working_line = line
                    for handler in [_split_imports_line, _remove_unused_non_fist_party_imports]:
                        working_line = handler(working_line)
                    print(working_line, end="")
            _format.format(bad_file)
        except AttributeError as e:
            failed_files.append((bad_file, e))
    if failed_files:
        raise Exception(
            "Failed to format files:\n"
            + "\n".join([f"{file}: {error}" for file, error in failed_files])
        )
