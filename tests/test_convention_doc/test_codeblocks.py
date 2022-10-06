"""Tests for the codeblocks in the convention document."""

import pathlib

import pytest


@pytest.fixture
def lint_codeblock(styleguide, tmp_path):
    """Fixture which runs the styleguide's `lint` subcommand when executed."""

    def run_linter(
        codeblock,
        *styleguide_args,
        # We ignore unused import warnings as most of the codeblocks which produce this warning
        # are just demonstrations of bad/good imports. Adding usage of the imports would add
        # code to trivial examples, detracting from the interesting lines.
        ignore_unused_imports=True,
    ):
        extend_ignore = [
            # Undefined name. Defining all the names in each example would detract from the
            # interesting lines.
            "F821",
            # Missing docstring in XYZ.
            "D1",
        ]
        if ignore_unused_imports:
            extend_ignore.append("F401")
        styleguide_args += ("--extend-ignore", ",".join(extend_ignore))

        test_file = tmp_path / "test.py"
        test_file.write_text(codeblock.contents, encoding="utf-8")
        return styleguide(
            "--config",
            pathlib.Path(__file__).parent / "codeblock_config.toml",
            "lint",
            *styleguide_args,
            test_file,
        )

    return run_linter


def test_rule_codeblock_uses_python(codeblock):
    """Test that the codeblock specifies "python" as its language."""
    assert codeblock.language == "python"


def test_rule_codeblocks_documents_bad_good_best(codeblock):
    """Test that the codeblock has a descriptor (first line comment) specifying Good/Bad/Best."""
    assert codeblock.descriptor in ("Good", "Bad", "Best")


def test_bad_codeblocks_document_lint_errors(lint_codeblock, bad_codeblock):
    """Test that "bad" codeblocks fail to lint and documents the resulting error codes."""
    if bad_codeblock.rule.is_automatically_enforced:
        result = lint_codeblock(
            bad_codeblock,
            "--format='%(code)s'",
            ignore_unused_imports=("F401" not in bad_codeblock.rule.error_codes),
        )
        assert not result, result.output

        error_codes = set(code.strip("'") for code in result.output.splitlines())
        assert error_codes
        expected_error_codes = set(bad_codeblock.rule.error_codes)
        error_codes_not_expected = error_codes - expected_error_codes
        assert error_codes.issubset(
            expected_error_codes
        ), f'"Bad" codeblock caused unexpected lint error - {error_codes_not_expected}'
    else:
        # "Bad" codeblock caused a lint error, but isn't marked as automatically enforced
        result = lint_codeblock(bad_codeblock)
        assert result, result.output


def test_good_codeblocks_have_no_lint_errors(lint_codeblock, good_codeblock):
    """Test that "good" codeblocks do not fail to lint."""
    result = lint_codeblock(good_codeblock)
    assert result, result.output


def test_best_codeblocks_have_no_lint_errors(lint_codeblock, best_codeblock):
    """Test that "best" codeblocks do not fail to lint."""
    result = lint_codeblock(best_codeblock)
    assert result, result.output
