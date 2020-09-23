import itertools

import toml

import pytest

TOO_LONG_LINE = "a_really_long_order = [" + ", ".join(itertools.repeat('"spam"', 10)) + "]\n"


@pytest.fixture
def styleguide_lint(styleguide, tmp_path, chdir):
    """Fixture which will run the styleguide with the "lint" subcommand.

    Both `base_args` and `lint_args` must be iterables which will be transformed into strings
    and passed on the cmd line in the following order: `<cmd> <base_args> lint <lint_args>.

    The fixture also ensures we run the linter from within the tmp_path directory.
    """

    def runner(base_args=[], lint_args=[]):
        return styleguide(*base_args, "lint", *lint_args)

    chdir(str(tmp_path))

    return runner


@pytest.fixture
def config_write(tmp_path):
    """Fixture which will write the specified data to a config file for the tool."""

    def writer(**config_data):
        (tmp_path / "pyproject.toml").write_text(
            toml.dumps(
                {"tool": {"ni-python-styleguide": config_data}},
            )
        )

    return writer


@pytest.fixture(
    params=[
        pytest.param(False, id="cmd_line"),
        pytest.param(True, id="config_file"),
    ]
)
def styleguide_lint_with_options(request, styleguide_lint, config_write, tmp_path):
    """Fixture which will run the styleguide with the "lint" subcommand, given the provided options.

    The options will be tested on the command line as well as in the config.
    `base_args` and `lint_args` are similar to the `styleguide_lint` fixture, with the exception of
    being mappings from option name to value.
    """

    def _to_cmd_line(item):
        return (f"--{item[0].replace('_', '-')}", item[1])

    def runner(base_args={}, lint_args={}):
        if request.param:
            base_args_strs = []
            lint_args_strs = []
            config_write(**base_args, **lint_args)

        else:
            base_args_strs = itertools.chain(*map(_to_cmd_line, base_args.items()))
            lint_args_strs = itertools.chain(*map(_to_cmd_line, lint_args.items()))

        return styleguide_lint(base_args=base_args_strs, lint_args=lint_args_strs)

    return runner


def test_lint__help_arg_prints_help(styleguide):
    result = styleguide("lint", "--help")

    assert result, result.output
    assert result.output.startswith("Usage:")


def test_lint__ignores_local_flake8_config(styleguide_lint, tmp_path):
    """Test that running lint ignores local flake8 config.

    We test this by creating a local config with a smaller (80) max line length than our styleguide
    enforces (100) and asserting the command passes with a line of length between 80 and 100.
    """
    (tmp_path / ".flake8").write_text(
        """
        [flake8]
        max_line_length = 80
        """
    )
    written_line = f'a_really_long_order = ["{", ".join(itertools.repeat("spam", 9))}]"\n'
    (tmp_path / "spam.py").write_text(written_line)

    result = styleguide_lint()

    assert result, result.output


def test_lint__with_one_file_arg(styleguide_lint, tmp_path):
    """Test that we can specify the file on the cmd-line"""
    (tmp_path / "spam.py").write_text(TOO_LONG_LINE)
    result = styleguide_lint(lint_args=[tmp_path / "spam.py"])

    assert not result, result.output
    assert "spam.py" in result.output


def test_lint__with_one_multiple_file_args(styleguide_lint, tmp_path):
    """Test that we can specify multiple files on the cmd-line"""
    (tmp_path / "spam1.py").write_text(TOO_LONG_LINE)
    (tmp_path / "spam2.py").write_text(TOO_LONG_LINE)
    result = styleguide_lint(lint_args=[tmp_path / "spam1.py", tmp_path / "spam2.py"])

    assert not result, result.output


def test_lint__specifying_file_only_lints_file(styleguide_lint, tmp_path):
    """Test that when we specify file(s) on the cmd line other files are not linted"""
    (tmp_path / "spam1.py").write_text(TOO_LONG_LINE)
    (tmp_path / "spam2.py").write_text("")  # empty
    result = styleguide_lint(lint_args=[tmp_path / "spam2.py"])

    assert result, result.output


def test_lint__no_args_lints_dir(styleguide_lint, tmp_path):
    """Test that when we specify no file(s) on the cmd line we lint the directory"""
    (tmp_path / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint()

    assert not result, result.output
    assert "spam.py" in result.output


def test_lint__no_args_lints_subdirs(styleguide_lint, tmp_path):
    """Test that when we specify no file(s) on the cmd line we lint subdirs"""
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint()

    assert not result, result.output
    assert "subdir/spam.py" in result.output.replace("\\", "/")


def test_lint__lignores_venv_by_default(styleguide_lint, tmp_path):
    """Test that we exclude ".venv" dir by default"""
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint()

    assert result, result.output


def test_lint__exclude__excludes_file(styleguide_lint_with_options, tmp_path):
    """Test that exclude option excludes a file"""
    (tmp_path / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint_with_options(base_args=dict(exclude="spam.py"))

    assert result, result.output


def test_lint__exclude__excludes_dir(styleguide_lint_with_options, tmp_path):
    """Test that exclude option excludes a dir"""
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint_with_options(base_args=dict(exclude="subdir"))

    assert result, result.output


def test_lint__exclude__overrides_default(styleguide_lint_with_options, tmp_path):
    """Test that specifying exclude option overrides the default exclude"""
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint_with_options(base_args=dict(exclude="eggs"))

    assert not result, result.output
    assert ".venv" in result.output


def test_lint__exclude__cmd_line_overrides_config(styleguide_lint, tmp_path, config_write):
    """Test that specifying exclude option on the cmd-line overrides the exclude in config"""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "spam.py").write_text(TOO_LONG_LINE)
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "spam.py").write_text(TOO_LONG_LINE)

    config_write(exclude="dir1")

    result = styleguide_lint(base_args=["--exclude", "dir2"])

    assert not result, result.output
    assert "dir1" in result.output


def test_lint__extend_exclude__extends_exclude(
    styleguide_lint_with_options, tmp_path, config_write
):
    """Test that extend-exclude adds to exclude"""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "spam.py").write_text(TOO_LONG_LINE)
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "spam.py").write_text(TOO_LONG_LINE)

    result = styleguide_lint_with_options(base_args=dict(exclude="dir1", extend_exclude="dir2"))

    assert result, result.output


@pytest.mark.parametrize(
    "verbosity_args",
    [
        "-v",
        "-vv",
        "-q",
        "-qq",
        "--verbose",
        "--quiet",
    ],
)
def test_lint__verbosity_args_allowed(styleguide_lint, verbosity_args):
    """Test that using verbosity flags doesnt have any fatal side-effects"""
    result = styleguide_lint(base_args=[verbosity_args])

    assert result, result.output
