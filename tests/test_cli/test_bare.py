def test_no_args_prints_help(styleguide):
    result = styleguide()

    assert result
    assert result.output.startswith("Usage:")


def test_help_prints_help(styleguide):
    result = styleguide("--help")

    assert result
    assert result.output.startswith("Usage:")
