import difflib
import pathlib
import typing

from ni_python_styleguide._utils import _constants


def diff(file1: pathlib.Path, file2: pathlib.Path) -> typing.Iterable[str]:
    """Return a diff between two files."""
    return _diff_lines(
        lines1=file1.read_text(encoding=_constants.DEFAULT_ENCODING).splitlines(),
        lines2=file2.read_text(encoding=_constants.DEFAULT_ENCODING).splitlines(),
        fromfile=str(file1),
        tofile=str(file2),
    )


def _diff_lines(
    lines1: typing.Iterable[str], lines2: typing.Iterable[str], fromfile="a", tofile="b"
) -> typing.Iterable[str]:
    raw = difflib.unified_diff(
        a=lines1,
        b=lines2,
        fromfile=fromfile,
        tofile=tofile,
    )

    result = []

    last_line: typing.Optional[str] = None
    for line in raw:
        if last_line and line:
            doing_a_substitution = last_line.startswith("-") and line.startswith("+")

            last_line_had_dangling_whitespace = last_line != last_line.rstrip()

            newline_matches_old_line_without_dangling_whitespace = (
                last_line[1:].rstrip() == line[1:]
            )

            need_to_highlight_whitespace_change = all(
                [
                    doing_a_substitution,
                    last_line_had_dangling_whitespace,
                    newline_matches_old_line_without_dangling_whitespace,
                ]
            )

            if need_to_highlight_whitespace_change:
                highlight = "^" * (len(last_line) - len(last_line.rstrip()))
                result.append("?" + " " * (len(line) - 1) + highlight)

        result.append(line)
        last_line = line

    return result
