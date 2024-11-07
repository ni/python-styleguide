import sys

import pytest
import pytest_mock
import toml


@pytest.fixture
def styleguide_bandit(styleguide_command):
    """Fixture which will run the styleguide with the "lint" subcommand.

    Both `base_args` and `lint_args` must be iterables which will be transformed into strings
    and passed on the cmd line in the following order: `<cmd> <base_args> lint <lint_args>.

    The base fixture also ensures we run the linter from within the tmp_path directory.
    """

    def runner(base_args=[], lint_args=[]):
        return styleguide_command(base_args=base_args, command="bandit", command_args=lint_args)

    return runner


@pytest.fixture
def fake_bandit(mocker: pytest_mock.MockerFixture):
    """Fixture which will mock the bandit.cli.main function."""
    mock = mocker.patch("bandit.cli.main.main")
    mock.config = {}

    def _cache_config():
        try:
            args = sys.argv
            conf_index = args.index("-c")
        except ValueError:
            return

        mock.config = toml.load(args[conf_index + 1])

    mock.side_effect = _cache_config

    yield mock


@pytest.fixture
def project_base_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        toml.dumps(
            {"tool": {"ni-python-styleguide": {}}},
        )
    )
    yield tmp_path


@pytest.fixture
def project_with_bandit_config(project_base_config):
    (project_base_config / "pyproject.toml").write_text(
        toml.dumps(
            {"tool": {"bandit": {"exclude": ["snapshots/"]}}},
        )
    )


def test_bandit_runs(project_with_bandit_config, styleguide_bandit, fake_bandit):
    styleguide_bandit()

    fake_bandit.assert_called_once()


def test_bandit_not_configured_gets_default_config(
    project_base_config, styleguide_bandit, fake_bandit
):
    styleguide_bandit()

    fake_bandit.assert_called_once()
    assert fake_bandit.config.get("tool", {}).get("bandit", {}).get("assert_used")


def test_bandit_configured_in_pyproj_gets_custom_config(
    project_with_bandit_config, styleguide_bandit, fake_bandit
):
    styleguide_bandit()

    fake_bandit.assert_called_once()
    assert fake_bandit.config.get("tool", {}).get("bandit", {}).get("exclude") == ["snapshots/"]
