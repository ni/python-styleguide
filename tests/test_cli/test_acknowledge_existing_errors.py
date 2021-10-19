"""Tests for the "acknowledge-existing-errors" subcommand of ni-python-styleguide."""

import pathlib
import shutil

import pytest

from ni_python_styleguide import _acknowledge_existing_errors


TEST_CASE_DIR = (
    pathlib.Path(__file__).parent.absolute() / "acknowledge_existing_errors_test_cases__snapshots"
)

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
    checker = _acknowledge_existing_errors._InMultiLineStringChecker(error_file=str(offending_file))

    result = checker.in_multiline_string(
        lineno=file_lineno,
    )

    assert result == expected_in_multiline


@pytest.mark.parametrize("test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()])
def test_given_bad_input_produces_expected_output(test_dir, snapshot, tmp_path, styleguide_command):
    """Test that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="acknowledge-existing-violations")

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_text(encoding="UTF-8")
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output.py")


@pytest.mark.parametrize("test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()])
def test_given_suppressed_file_linter_does_not_error(test_dir, styleguide_command, chdir):
    """Test linter does not error on output from suppresion."""
    chdir(test_dir)

    # lint the output file - we don't suppress BLK100, so it's not one we expect to pass
    output = styleguide_command(
        command="lint", command_args=["expected_output.py", "--extend-ignore=BLK100"]
    )

    assert output.exit_code in (True, 0), f"Error in running:\n{output.output}\n\n"
