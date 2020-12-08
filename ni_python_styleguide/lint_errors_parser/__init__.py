import re
from collections import namedtuple

LintError = namedtuple("LintError", ["file", "line", "column", "code", "explanation"])


def _to_lint_error(file: str, line: str, column: str, code: str, explanation: str, **kwargs):
    return LintError(
        file=file, line=int(line), column=int(column), code=code, explanation=explanation, **kwargs
    )


def parse(line):
    r"""
    >>> parse(r'source\arfile.py:55:16: BLK100 Black would make changes.')
    LintError(file='source\\arfile.py', line=55, column=16, code='BLK100', explanation='Black would make changes.')

    >>> parse(r"source\rpmfile\__init__.py:13:1: F401 'functools.wraps' imported but unused")
    LintError(file='source\\rpmfile\\__init__.py', line=13, column=1, code='F401', explanation="'functools.wraps' imported but unused")
    """
    p = Parser()
    return p.parse(line)


class Parser:
    __MATCHER = re.compile(
        r"^(?P<file>[\w\\\.]+):(?P<line>\d+):(?P<column>\d+): (?P<code>\w+) (?P<explanation>.+)"
    )

    def parse(self, line):
        data = Parser.__MATCHER.search(line)
        if not data:
            return None
        result = _to_lint_error(**data.groupdict())
        return result

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
