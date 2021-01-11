from ni_python_styleguide import _acknowledge_existing_errors

import pytest

example_file_lines = [
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
    input_lines = example_file_lines
    file_lineno = lineno + 1  # we number files 1-n, not 0-n
    offending_file = tmp_path / "python_file.py"
    offending_file.write_text("\n".join(input_lines))

    result = _acknowledge_existing_errors._in_multiline_string(
        error_file=str(offending_file),
        lineno=file_lineno,
    )

    assert result == expected_in_multiline
