import logging
import re
from collections import namedtuple

LintError = namedtuple("LintError", ["file", "line", "column", "code", "explanation"])


def parse(line):
    r"""
    Parse line into :class:`LintError`.

    >>> parse(r'source\arfile.py:55:16: BLK100 Black would make changes.')
    LintError(file='source\\arfile.py', line=55, column=16, code='BLK100', explanation='Black would make changes.')

    >>> parse(r"source\rpmfile\__init__.py:13:1: F401 'functools.wraps' imported but unused")
    LintError(file='source\\rpmfile\\__init__.py', line=13, column=1, code='F401', explanation="'functools.wraps' imported but unused")

    >>> parse(r"expected_output.py:77:6: N802 function name 'method_withBadName_with_bad_params_on_multiple_lines_1' should be lowercase")
    LintError(file='expected_output.py', line=77, column=6, code='N802', explanation="function name 'method_withBadName_with_bad_params_on_multiple_lines_1' should be lowercase")

    >>> parse(r"./tests/test_cli/acknowledge_existing_errors_test_cases__snapshots/doc_line_tests/expected_output.py:1:1: D100 Missing docstring in public module")
    LintError(file='./tests/test_cli/acknowledge_existing_errors_test_cases__snapshots/doc_line_tests/expected_output.py', line=1, column=1, code='D100', explanation='Missing docstring in public module')
    """  # NOQA W505: doc line too long (115 > 100 characters)
    p = Parser()
    return p.parse(line)


class Parser:
    """Lint errors parser."""

    __MATCHER = re.compile(
        r"^(?P<file>[\w\\/\.]+):(?P<line>\d+):(?P<column>\d+): (?P<code>\w+) (?P<explanation>.+)"
    )

    @staticmethod
    def _to_lint_error(file: str, line: str, column: str, code: str, explanation: str, **kwargs):
        return LintError(
            file=file,
            line=int(line),
            column=int(column),
            code=code,
            explanation=explanation,
            **kwargs
        )

    def parse(self, line):
        """Parse `line` and return a :class:`LintError`.

        :param line: the line to parse
        :return: lint error as metada object
        :rtype: LintError
        """
        data = Parser.__MATCHER.search(line)
        logging.debug("parsing line: %s, yielded %s", line, data)
        if not data:
            return None
        result = Parser._to_lint_error(**data.groupdict())
        return result
