"""Useful fixtures for testing the convention document."""

import pytest

from tests.test_convention_doc import doctypes


@pytest.fixture
def sections():
    """All convention sections."""
    return doctypes.SECTIONS


@pytest.fixture
def subsections():
    """All convention subsections."""
    return doctypes.SUBSECTIONS


@pytest.fixture
def rules():
    """All convention rules."""
    return doctypes.RULES


@pytest.fixture(
    scope="module",
    params=[pytest.param(section, id=section.identifier) for section in doctypes.SECTIONS],
)
def section(request):
    """Each convention section."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(subsection, id=subsection.identifier) for subsection in doctypes.SUBSECTIONS
    ],
)
def subsection(request):
    """Each convention subsection."""
    return request.param


@pytest.fixture(
    scope="module",
    params=[pytest.param(rule, id=rule.identifier) for rule in doctypes.RULES],
)
def rule(request):
    """Each convention rule."""
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
    """Each convention codeblock."""
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
    """Each convention codeblock marked "Bad"."""
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
    """Each convention codeblock marked "Good"."""
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
    """Each convention codeblock marked "Best"."""
    return request.param
