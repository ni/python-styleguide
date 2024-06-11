"""Tests for the "fix" subcommand of ni-python-styleguide."""

import pathlib
import shutil

import pytest

TEST_CASE_DIR = pathlib.Path(__file__).parent.absolute() / "fix_test_cases__snapshots"

TEST_CASES = [x for x in TEST_CASE_DIR.iterdir() if x.is_dir() and (x / "input.py").is_file()]


@pytest.fixture()
def example_pyproject_file(tmp_path):
    """Provides the current project's pyproject.toml file to tests as an example."""
    in_file = next(
        (
            parent / "pyproject.toml"
            for parent in TEST_CASE_DIR.parents
            if (parent / "pyproject.toml").is_file()
        ),
        "pyproject.toml",
    )
    out_file = tmp_path / "pyproject.toml"
    shutil.copyfile(in_file, out_file)
    return out_file


@pytest.mark.parametrize("test_dir", TEST_CASES)
def test_given_bad_input__fix__produces_expected_output_simple(
    test_dir, snapshot, tmp_path, styleguide_command, example_pyproject_file
):
    """Tests that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="fix")

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_text(encoding="UTF-8")
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output.py.txt")


@pytest.mark.parametrize("test_dir", TEST_CASES)
def test_given_bad_input__fix__produces_expected_output_aggressive(
    test_dir, snapshot, tmp_path, styleguide_command, example_pyproject_file
):
    """Tests that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)
    test_loading_file = tmp_path / ".venv/file_with_non_unicode_chars.py"
    test_loading_file.parent.mkdir(parents=True, exist_ok=True)
    test_loading_file.write_text("Förward to victory!", encoding="ISO 8859-1")

    output = styleguide_command(command="fix", command_args=["--aggressive"])

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_text(encoding="UTF-8")
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output__aggressive.py")
