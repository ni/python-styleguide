"""Tests for the "acknowledge-existing-errors" subcommand of ni-python-styleguide."""

import pathlib

from ni_python_styleguide import _acknowledge_existing_errors

import pytest

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

    result = _acknowledge_existing_errors._in_multiline_string(
        error_file=str(offending_file),
        lineno=file_lineno,
    )

    assert result == expected_in_multiline


@pytest.fixture
def styleguide_acknowledge(styleguide, tmp_path, chdir):
    """Fixture which will run the styleguide with the "acknowledge-existing-violations" subcommand.

    Both `base_args` and `lint_args` must be iterables which will be transformed into strings
    and passed on the cmd line in the following order:
    `<cmd> <base_args> acknowledge-existing-violations <lint_args>.

    The fixture also ensures we run the command from within the tmp_path directory.
    """

    def runner(base_args=[], lint_args=[]):
        return styleguide(*base_args, "acknowledge-existing-violations", *lint_args)

    chdir(str(tmp_path))

    return runner


@pytest.fixture
def styleguide_lint(styleguide, tmp_path, chdir):
    """Fixture which will run the styleguide with the "lint" subcommand.

    Both `base_args` and `lint_args` must be iterables which will be transformed into strings
    and passed on the cmd line in the following order: `<cmd> <base_args> lint <lint_args>.
    """

    def runner(base_args=[], lint_args=[]):
        return styleguide(*base_args, "lint", *lint_args)

    return runner


@pytest.mark.parametrize("test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()])
def test_given_bad_input_produces_expected_output(
    test_dir, snapshot, tmp_path, styleguide_acknowledge
):
    """Test that suppresion yields expected_output file."""
    in_file = test_dir / "bad_input.py"
    out_file = tmp_path / "bad_input.py"
    raw_file = in_file.read_text()
    out_file.write_text(raw_file)

    output = styleguide_acknowledge()

    assert output.exit_code == 0, f"Error in running:\n{output}"
    result = out_file.read_text()
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "expected_output.py")


@pytest.mark.parametrize("test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()])
def test_given_suppressed_file_linter_does_not_error(test_dir, styleguide_lint, chdir):
    """Test linter does not error on output from suppresion."""
    chdir(test_dir)

    # lint the output file - we don't suppress BLK100, so it's not one we expect to pass
    output = styleguide_lint(lint_args=["expected_output.py", "--extend-ignore=BLK100"])

    assert output.exit_code == 0, f"Error in running:\n{output.output}\n\n"
