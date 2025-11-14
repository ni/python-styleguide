"""Tests for the "acknowledge-existing-errors" subcommand of ni-python-styleguide."""

import pathlib
import shutil

import pytest

MODULE_DIR = pathlib.Path(__file__).parent.absolute()
TEST_CASE_DIR = (
    MODULE_DIR / "acknowledge_existing_errors_test_cases__snapshots"
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
    snapshot.assert_match(result, "output.py.txt")


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
            "output.py.txt",
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


@pytest.mark.parametrize("cmd_args", [[], ["--aggressive"]], ids=["normal", "aggressive"])
def test_given_folder_with_multiple_files_linter_does_not_error(cmd_args, tmp_path, styleguide_command, chdir):
    in_dir = MODULE_DIR / "acknowledge_existing_errors_multiple_files" / "input"
    test_dir = tmp_path / "input"
    shutil.copytree(in_dir, test_dir)
    chdir(tmp_path)

    output = styleguide_command(command="acknowledge-existing-violations", command_args=cmd_args)

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"



def test_given_folder_with_multiple_files_acknowledged__does_not_error(tmp_path, styleguide_command, chdir):
    in_dir = MODULE_DIR / "acknowledge_existing_errors_multiple_files" / "input"
    test_dir = tmp_path / "input"
    shutil.copytree(in_dir, test_dir)
    chdir(tmp_path)
    styleguide_command(command="acknowledge-existing-violations", command_args=["--aggressive"])

    output = styleguide_command(command="lint", command_args=[])

    assert output.exit_code in (True, 0), f"Error in running:\n{output.output}\n\n"
