import pytest


@pytest.fixture
def lint_codeblock(styleguide, tmp_path):
    def run_linter(codeblock, *styleguide_args):
        test_file = tmp_path / "test.py"
        test_file.write_text(codeblock.contents, encoding="utf-8")
        return styleguide("lint", test_file, *styleguide_args)

    return run_linter


def test_rule_codeblock_uses_python(codeblock):
    assert codeblock.language == "python"


def test_rule_codeblocks_documents_bad_good_best(codeblock):
    assert codeblock.descriptor in ("Good", "Bad", "Best")


def test_bad_codeblocks_document_lint_errors(lint_codeblock, bad_codeblock, capsys):
    if bad_codeblock.rule.is_automatically_enforced:
        assert not lint_codeblock(
            bad_codeblock, "--format", "'%(code)s'"
        ), 'Expected automatically enforced "bad" codeblock to cause lint error'

        captured = capsys.readouterr()
        error_codes = set(
            error_code.strip("'") for error_code in captured.out.strip().split("\n")
        )

        assert error_codes.issubset(
            set(bad_codeblock.rule.error_codes)
        ), '"Bad" codeblock caused unexpected lint error'
    else:
        # You can check stdout from the test results to see the lint errors
        assert lint_codeblock(
            bad_codeblock
        ), '"Bad" codeblock caused a lint error, but isn\'t marked as automatically enforced'


def test_good_codeblocks_have_no_lint_errors(lint_codeblock, good_codeblock):
    assert lint_codeblock(good_codeblock), '"Good" codeblock caused lint error'


def test_best_codeblocks_have_no_lint_errors(lint_codeblock, best_codeblock):
    assert lint_codeblock(best_codeblock), '"Best" codeblock caused lint error'
