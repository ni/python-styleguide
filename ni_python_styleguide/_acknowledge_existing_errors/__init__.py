import logging
import pathlib
import re
from collections import defaultdict

from ni_python_styleguide import _format
from ni_python_styleguide import _lint
from ni_python_styleguide._acknowledge_existing_errors import _lint_errors_parser

_module_logger = logging.getLogger(__name__)

EXCLUDED_ERRORS = {
    "BLK100",
}

DEFAULT_ENCODING = "UTF-8"


class _InMultiLineStringChecker:
    def __init__(self, error_file):
        self._error_file = pathlib.Path(error_file)
        self._values = []
        self._load_lines()

    @property
    def values(self):
        return self._values

    def in_multiline_string(self, lineno):
        return self._values[lineno - 1]  # 0 indexed, but we number files 1 indexed

    @staticmethod
    def _count_multiline_string_endings_in_line(line):
        return line.count('"""'), line.count("'''")

    def _load_lines(self):
        in_file = self._error_file.read_text(encoding=DEFAULT_ENCODING).splitlines()
        current_count = [0, 0]
        for line in in_file:
            type1, type2 = _InMultiLineStringChecker._count_multiline_string_endings_in_line(line)
            current_count[0] += type1
            current_count[1] += type2

            code_part_of_line = line
            if "#" in line:
                code_part_of_line = line.split("#", maxsplit=1)[0]

            # if occurrences of multiline string markers is odd, this must be in a multiline
            #  or, if line continuation token is on the ending, assume in a multiline statement
            self._values.append(
                any([part % 2 == 1 for part in current_count])
                or code_part_of_line.strip().endswith("\\")
            )


def _add_noqa_to_line(lineno, code_lines, error_code, explanation):
    line = code_lines[lineno]
    old_line_ending = "\n" if line.endswith("\n") else ""
    line = line.rstrip("\n")

    if f"noqa {error_code}" not in line:
        prefix = "  " if line.strip() else ""
        line += f"{prefix}# noqa {error_code}: {explanation} (auto-generated noqa)"

    code_lines[lineno] = line + old_line_ending


def _filter_suppresion_from_line(line: str):
    if "(auto-generated noqa)" in line:
        return re.sub(r"# noqa .+\(auto-generated noqa\)", "", line).rstrip()
    else:
        return line


def _get_lint_errors_to_process(exclude, app_import_names, extend_ignore, file_or_dir):
    lint_errors = _lint.get_lint_output(
        format=None,
        qs_or_vs=None,
        exclude=exclude,
        app_import_names=app_import_names,
        extend_ignore=extend_ignore,
        file_or_dir=file_or_dir,
    ).splitlines()
    parsed_errors = map(_lint_errors_parser.parse, lint_errors)
    parsed_errors = filter(None, parsed_errors)
    lint_errors_to_process = [error for error in parsed_errors if error.code not in EXCLUDED_ERRORS]
    return lint_errors_to_process


def acknowledge_lint_errors(
    exclude, app_import_names, extend_ignore, file_or_dir, *_, aggressive=False
):
    """Add a "noqa" comment for each of existing errors (unless excluded).

    Excluded error (reason):
    BLK100 - run black
    """
    lint_errors_to_process = _get_lint_errors_to_process(
        exclude,
        app_import_names,
        extend_ignore,
        [pathlib.Path(file_or_dir_) for file_or_dir_ in file_or_dir or "."],
    )

    lint_errors_by_file = defaultdict(list)
    for error in lint_errors_to_process:
        lint_errors_by_file[pathlib.Path(error.file)].append(error)

    failed_files = []
    for bad_file, errors_in_file in lint_errors_by_file.items():
        _suppress_errors_in_file(bad_file, errors_in_file, encoding=DEFAULT_ENCODING)

        if aggressive:
            # some cases are expected to take up to 4 passes, making this 2x rounded
            per_file_format_iteration_limit = 10
            for _ in range(per_file_format_iteration_limit):
                # format the files - this may move the suppression off the correct lines
                #  Note: due to Github pycodestyle#868, we have to format, change, format
                #   (check if that time made changes)
                # -  else we wind up with lambda's going un-suppressed
                # and/or not re-formatted (to fail later)
                _format.format(bad_file)

                # re-apply suppressions on correct lines
                _remove_auto_suppressions_from_file(bad_file)
                current_lint_errors = _get_lint_errors_to_process(
                    exclude, app_import_names, extend_ignore, [bad_file]
                )
                _suppress_errors_in_file(bad_file, current_lint_errors, encoding=DEFAULT_ENCODING)

                changed = _format.format_check(bad_file)
                if not changed:  # are we done?
                    break
            else:
                failed_files.append(
                    f"Could not handle suppressions/formatting of file {bad_file} after maximum number of tries ({per_file_format_iteration_limit})"
                )
                _module_logger.warning("Max tries reached on %s", bad_file)
    if failed_files:
        raise RuntimeError("Could not handle some files:\n" + "\n\n".join(failed_files) + "\n\n\n")


def _remove_auto_suppressions_from_file(file):
    lines = file.read_text(encoding=DEFAULT_ENCODING).splitlines()
    stripped_lines = [_filter_suppresion_from_line(line) for line in lines]
    file.write_text("\n".join(stripped_lines) + "\n", encoding=DEFAULT_ENCODING)


def _suppress_errors_in_file(bad_file, errors_in_file, encoding):
    path = pathlib.Path(bad_file)
    lines = path.read_text(encoding=encoding).splitlines(keepends=True)
    # sometimes errors are reported on line 1 for empty files.
    # to make suppressions work for those cases, add an empty line.
    if len(lines) == 0:
        lines = ["\n"]
    multiline_checker = _InMultiLineStringChecker(error_file=bad_file)

    # to avoid double marking a line with the same code, keep track of lines and codes
    handled_lines = defaultdict(list)
    for error in errors_in_file:
        skip = 0

        while error.line + skip < len(lines) and multiline_checker.in_multiline_string(
            lineno=error.line + skip
        ):
            # find when the multiline ends
            skip += 1

        cached_key = f"{error.file}:{error.line + skip}"
        if error.code in handled_lines[cached_key]:
            _module_logger.warning(
                "Multiple occurrences of error %s code were logged for %s:%s, only supressing first",
                error.code,
                error.file,
                error.line + skip,
            )
            continue

        handled_lines[cached_key].append(error.code)

        _add_noqa_to_line(
            lineno=error.line - 1 + skip,
            code_lines=lines,
            error_code=error.code,
            explanation=error.explanation,
        )

    path.write_text("".join(lines), encoding=encoding)
