"""Test that the CLI is functional and behaving as expected"""

import pytest


@pytest.mark.parametrize(
    "args",
    (
        ["--version"],
        ["baseline", __file__],
        ["code", "E101"],
        ["codes", "pycodestyle"],
        ["lint", __file__],
        ["missed"],
        ["plugins"],
        ["yesqa", __file__],
    ),
    ids=lambda p: p[0],
)
def test_command_valid(styleguide, args):
    """Test that our thin wrapper doesnt cause any issues with flakehell"""

    assert styleguide(*args)
