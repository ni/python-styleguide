from ni_python_styleguide import acknowledge_existing_errors

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
    "input_lines,lineno,expected_in_multiline",
    (
        (example_file_lines, 1, False),
        (example_file_lines, 2, True),
        (example_file_lines, 3, True),
        (example_file_lines, 4, False),
        (example_file_lines, 5, False),
        (example_file_lines, 6, True),
        (example_file_lines, 7, True),
        (example_file_lines, 8, True),
        (example_file_lines, 9, False),
        (example_file_lines, 10, False),
    ),
)
def test_can_acurately_detect_if_in_multiline_string(
    input_lines, lineno, expected_in_multiline, tmp_path
):
    offending_file = tmp_path / "python_file.py"
    offending_file.write_text("\n".join(input_lines))

    result = acknowledge_existing_errors._in_multiline_string(
        error_file=str(offending_file),
        lineno=lineno,
    )

    assert result == expected_in_multiline
