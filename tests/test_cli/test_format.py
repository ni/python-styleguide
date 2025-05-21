"""Tests for the "acknowledge-existing-errors" subcommand of ni-python-styleguide."""

import pathlib
import shutil
import typing

import pytest
from pytest_snapshot.plugin import Snapshot

TEST_CASE_DIR = pathlib.Path(__file__).parent.absolute() / "format_test_cases__snapshots"


@pytest.mark.parametrize(
    "test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()], ids=lambda o: o.name
)
def test_given_input_file__produces_expected_output_simple(
    test_dir, snapshot: Snapshot, tmp_path: pathlib.Path, styleguide_command: callable
):
    """Tests that suppresion yields expected_output file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="format")

    assert output.exit_code in (True, 0), f"Error in running:\n{output}"
    result = test_file.read_bytes()
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output.py")


@pytest.mark.parametrize(
    "test_dir", [x for x in TEST_CASE_DIR.iterdir() if x.is_dir()], ids=lambda o: o.name
)
def test_given_input_file__produces_expected_output_diff(
    test_dir, snapshot: Snapshot, tmp_path: pathlib.Path, styleguide_command: callable
):
    """Tests diff mode on file outputs expected."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="format", command_args=["--diff"])

    assert output.exception is None
    result = output.stdout.replace(str(test_file), in_file.relative_to(TEST_CASE_DIR).as_posix())
    snapshot.snapshot_dir = test_dir
    snapshot.assert_match(result, "output.diff")


@pytest.mark.parametrize(
    "test_dir",
    [x for x in TEST_CASE_DIR.iterdir() if x.is_dir() if x.name != "blank_file"],
    ids=lambda o: o.name,
)
@pytest.mark.parametrize("command_args", [["--check"], ["--check", "--diff"]])
def test_given_bad_input_file__check_mode__fails(
    test_dir, tmp_path: pathlib.Path, styleguide_command: callable, command_args: typing.List[str]
):
    """Tests check mode fails on bad file."""
    in_file = test_dir / "input.py"
    test_file = tmp_path / "input.py"
    shutil.copyfile(in_file, test_file)

    output = styleguide_command(command="format", command_args=command_args)

    assert output.exception is not None, f"Should error running:\n{output}"
