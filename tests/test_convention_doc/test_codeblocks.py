import json

import pytest


@pytest.fixture
def lint_codeblock(styleguide, tmp_path):
    def run_linter(codeblock, *styleguide_args):
        test_file = tmp_path / "test.py"
        test_file.write_text(codeblock.contents, encoding="utf-8")
        return styleguide("lint", *styleguide_args, test_file)

    return run_linter


def test_rule_codeblock_uses_python(codeblock):
    assert codeblock.language == "python"


def test_rule_codeblocks_documents_bad_good_best(codeblock):
    assert codeblock.descriptor in ("Good", "Bad", "Best")


def test_bad_codeblocks_document_lint_errors(lint_codeblock, bad_codeblock):
    if bad_codeblock.rule.is_automatically_enforced:
        result = lint_codeblock(bad_codeblock, "--format='%(code)s'")
        assert not result, result.output

        error_codes = set(code.strip("'") for code in result.output.splitlines())
        assert error_codes
        assert error_codes.issubset(
            set(bad_codeblock.rule.error_codes)
        ), '"Bad" codeblock caused unexpected lint error'
    else:
        # "Bad" codeblock caused a lint error, but isn't marked as automatically enforced
        result = lint_codeblock(bad_codeblock)
        assert result, result.output


def test_good_codeblocks_have_no_lint_errors(lint_codeblock, good_codeblock):
    result = lint_codeblock(good_codeblock)
    assert result, result.output


def test_best_codeblocks_have_no_lint_errors(lint_codeblock, best_codeblock):
    result = lint_codeblock(best_codeblock)
    assert result, result.output
