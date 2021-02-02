from collections import defaultdict
import logging
import re
import pathlib

import ni_python_styleguide._lint_errors_parser


class _in_multiline_string_checker:
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
        return line.count('"""') + line.count("'''")

    def _load_lines(self):
        in_file = self._error_file.read_text().splitlines()
        current_count = 0
        for line in in_file:
            line_value = (
                current_count
                + _in_multiline_string_checker._count_multiline_string_endings_in_line(line)
            )
            # if occurances of multiline string markers is odd, this must be in a multiline
            self._values.append(line_value % 2 == 1)
            current_count = line_value


def _add_noqa_to_line(lineno, filepath, error_code, explanation):
    with open(filepath, mode="r") as cache_file:
        code = cache_file.readlines()

    line = code[lineno]
    line_had_newline = line.endswith("\n")
    line = line.rstrip("\n")

    existing_suppression = re.search(r"noqa (?P<existing_suppresions>[\w\d]+\: [\w\W]+?) -", line)
    if existing_suppression:
        before = existing_suppression.groupdict()["existing_suppresions"]
        if error_code not in before:
            line = line.replace(before, before + f", {error_code}: {explanation}") + "\n"
    else:
        line += f"  # noqa {error_code}: {explanation} (auto-generated noqa)\n"
    if not line_had_newline:
        line.rstrip("\n")
    code[lineno] = line

    with open(filepath, mode="w") as out_file:
        for line in code:
            out_file.write(line)


def acknowledge_lint_errors(lint_errors):
    """Add a "noqa" comment for each of existing errors (unless excluded).

    Excluded error (reason):
    BLK100 - run black
    """
    EXCLUDED_ERRORS = {
        "BLK100",
    }
    parsed_errors = map(ni_python_styleguide._lint_errors_parser.parse, lint_errors)
    parsed_errors = filter(None, parsed_errors)
    lint_errors_to_process = [error for error in parsed_errors if error not in EXCLUDED_ERRORS]

    # to avoid double marking a line with the same code, keep track of lines and codes
    handled_lines = defaultdict(list)
    for error in lint_errors_to_process:
        skip = 0

        multiline_checker = _in_multiline_string_checker(error_file=error.file)
        while multiline_checker.in_multiline_string(lineno=error.line + skip):
            # find when the multiline ends
            skip += 1

        cached_key = f"{error.file}:{error.line + skip}"
        if error.code in handled_lines.get(cached_key, []):
            logging.warning(
                "Multiple occurances of error %s code were logged for %s:%s, only suprressing first",
                error.code,
                error.file,
                error.line + skip,
            )
            continue

        handled_lines[cached_key].append(error.code)

        _add_noqa_to_line(
            lineno=error.line - 1 + skip,
            filepath=error.file,
            error_code=error.code,
            explanation=error.explanation,
        )
