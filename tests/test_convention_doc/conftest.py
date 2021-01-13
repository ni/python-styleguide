"""Useful fixtures for testing the convention document."""

import pytest

from tests.test_convention_doc import doctypes


@pytest.fixture
def sections():
    """Fixture with each convention section."""
    return doctypes.SECTIONS


@pytest.fixture
def subsections():
    """Fixture with each convention subsection."""
    return doctypes.SUBSECTIONS


@pytest.fixture
def rules():
    """Fixture with each convention rule."""
    return doctypes.RULES


@pytest.fixture(
    scope="module",
    params=[pytest.param(section, id=section.identifier) for section in doctypes.SECTIONS],
)
def section(request):
    """Parametrized fixture of each convention section."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(subsection, id=subsection.identifier) for subsection in doctypes.SUBSECTIONS
    ],
)
def subsection(request):
    """Parametrized fixture of each convention subsection."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[pytest.param(rule, id=rule.identifier) for rule in doctypes.RULES],
)
def rule(request):
    """Parametrized fixture of each convention rule."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(codeblock, id=f"{rule.identifier}-{codeblock.descriptor}")
        for rule in doctypes.RULES
        for codeblock in rule.codeblocks
    ],
)
def codeblock(request):
    """Parametrized fixture of each convention codeblock."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(codeblock, id=f"{rule.identifier}-{codeblock.descriptor}")
        for rule in doctypes.RULES
        for codeblock in rule.codeblocks
        if codeblock.descriptor == "Bad"
    ],
)
def bad_codeblock(request):
    """Parametrized fixture of each convention codeblock marked "Bad"."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(codeblock, id=f"{rule.identifier}-{codeblock.descriptor}")
        for rule in doctypes.RULES
        for codeblock in rule.codeblocks
        if codeblock.descriptor == "Good"
    ],
)
def good_codeblock(request):
    """Parametrized fixture of each convention codeblock marked "Good"."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(codeblock, id=f"{rule.identifier}-{codeblock.descriptor}")
        for rule in doctypes.RULES
        for codeblock in rule.codeblocks
        if codeblock.descriptor == "Best"
    ],
)
def best_codeblock(request):
    """Parametrized fixture of each convention codeblock marked "Best"."""
    return request.param
