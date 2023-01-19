"""Tests for the bare CLI (executing the script without a subcommand)."""


def test_no_args_prints_help(styleguide):
    """Tests that running the styleguide without any arguments prints the help info."""
    result = styleguide()

    assert result
    assert result.output.startswith("Usage:")


def test_help_prints_help(styleguide):
    """Tests that running the styleguide with "--help" prints the help info."""
    result = styleguide("--help")

    assert result
    assert result.output.startswith("Usage:")
