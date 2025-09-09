"""Tests for the "_get_application_import_names" method of _cli.py."""

import pytest

from ni_python_styleguide._cli import _get_application_import_names


@pytest.mark.parametrize(
    "pyproject_obj, expected_names",
    [
        (
            {
                "tool": {
                    "ni-python-styleguide": {
                        "application-import-names": "ain1,ain2"
                    },
                    "poetry": {
                        "name": "tool.poetry.name"
                    }
                },
                "project": {
                    "import-names": ["import-names1", "import-names2"],
                    "name": "project.name"
                }
            },
            "ain1,ain2,tests"
        ),
        (
            {
                "tool": {
                    "poetry": {
                        "name": "tool.poetry.name"
                    }
                },
                "project": {
                    "import-names": ["import-names1", "import-names2"],
                    "name": "project.name"
                }
            },
            "import-names1,import-names2,tests"
        ),
        (
            {
                "tool": {
                    "poetry": {
                        "name": "tool.poetry.name"
                    }
                },
                "project": {
                    "name": "project.name"
                }
            },
            "project.name,tests"
        ),
        (
            {
                "tool": {
                    "poetry": {
                        "name": "tool.poetry.name"
                    }
                }
            },
            "tool.poetry.name,tests"
        )
    ],
)
def test_get_application_import_names_returns_valid_data(pyproject_obj, expected_names):
    """Tests that _get_application_import_names returns valid data."""
    result = _get_application_import_names(pyproject_obj)
    assert result == expected_names
