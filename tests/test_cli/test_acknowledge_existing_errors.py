"""Tests for the "acknowledge-existing-errors" subcommand of ni-python-styleguide."""

import pathlib
import shutil

import pytest

TEST_CASE_DIR = (
    pathlib.Path(__file__).parent.absolute() / "acknowledge_existing_errors_test_cases__snapshots"
)


@pytest.mark.parametrize(
    "test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()], ids=lambda o: o.name
)
def test_given_bad_input_produces_expected_output_simple(
    test_dir, snapshot, tmp_path, styleguide_command
):
    """Tests that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="acknowledge-existing-violations")

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_text(encoding="UTF-8")
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output.py")


@pytest.mark.parametrize(
    "test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()], ids=lambda o: o.name
)
def test_given_bad_input_produces_expected_output_aggressive(
    test_dir, snapshot, tmp_path, styleguide_command
):
    """Tests that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(
        command="acknowledge-existing-violations", command_args=["--aggressive"]
    )

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_text(encoding="UTF-8")
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output__aggressive.py")


@pytest.mark.parametrize(
    "test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()], ids=lambda o: o.name
)
@pytest.mark.parametrize(
    "test_file,additional_args",
    [
        pytest.param(
            "output.py",
            ["--extend-ignore=BLK100"],
            id="output_ignore_black",
        ),  # we don't suppress BLK100, so it's not one we expect to pass
        pytest.param("output__aggressive.py", [], id="output_aggressive"),
    ],
)
def test_given_suppressed_file_linter_does_not_error(
    test_dir, test_file, additional_args, styleguide_command, chdir
):
    """Tests linter does not error on output from suppresion."""
    chdir(test_dir)

    output = styleguide_command(command="lint", command_args=[test_file, *additional_args])

    assert output.exit_code in (True, 0), f"Error in running:\n{output.output}\n\n"
