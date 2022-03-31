"""Tests for the "fix" subcommand of ni-python-styleguide."""

import pathlib
import shutil

import pytest


TEST_CASE_DIR = pathlib.Path(__file__).parent.absolute() / "fix_test_cases__snapshots"

@pytest.fixture()
def example_pyproject_file(tmp_path):
    in_file = next((parent / "pyproject.toml" for parent in TEST_CASE_DIR.parents if (parent / "pyproject.toml").is_file()), "pyproject.toml")
    out_file = tmp_path / "pyproject.toml"
    shutil.copyfile(in_file, out_file)
    return out_file


@pytest.mark.parametrize("test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()])
def test_given_bad_input__fix__produces_expected_output_simple(
    test_dir, snapshot, tmp_path, styleguide_command, example_pyproject_file
):
    """Test that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="fix")

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_text(encoding="UTF-8")
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output.py")
