"""Test the _utils submodule."""
import pathlib

import pytest

from ni_python_styleguide import _utils

EXAMPLE_FILE_LINES = [
    "import pytest",
    "apple='''",
    "test",
    "'''",
    "x = 5",
    'orange="""',
    "lorem ipsum",
    "dolor sit amet",
    '"""',
    "move_files()",
]

MODULE_DIR = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "lineno,expected_in_multiline",
    enumerate(
        [
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
        ]
    ),
)
def test_can_acurately_detect_if_in_multiline_string(lineno, expected_in_multiline, tmp_path):
    """Assert can accurately detect multiline strings."""
    input_lines = EXAMPLE_FILE_LINES
    file_lineno = lineno + 1  # we number files 1-n, not 0-n
    offending_file = tmp_path / "python_file.py"
    offending_file.write_text("\n".join(input_lines))
    checker = _utils.string_helpers.InMultiLineStringChecker(error_file=str(offending_file))

    result = checker.in_multiline_string(
        lineno=file_lineno,
    )

    assert result == expected_in_multiline
