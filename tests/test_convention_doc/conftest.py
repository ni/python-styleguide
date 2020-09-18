import pytest

from tests.test_convention_doc import doctypes


@pytest.fixture
def sections():
    return doctypes.SECTIONS


@pytest.fixture
def subsections():
    return doctypes.SUBSECTIONS


@pytest.fixture
def rules():
    return doctypes.RULES


@pytest.fixture(
    scope="module",
    params=[pytest.param(section, id=section.identifier) for section in doctypes.SECTIONS],
)
def section(request):
    return request.param


@pytest.fixture(
    scope="module",
    params=[
        pytest.param(subsection, id=subsection.identifier) for subsection in doctypes.SUBSECTIONS
    ],
)
def subsection(request):
    return request.param


@pytest.fixture(
    scope="module",
    params=[pytest.param(rule, id=rule.identifier) for rule in doctypes.RULES],
)
def rule(request):
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
    return request.param
