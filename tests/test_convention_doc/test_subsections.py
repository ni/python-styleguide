"""Tests for the convention subsections"""

import re

import pytest

from tests.test_convention_doc import doctypes


@pytest.fixture(
    scope="module",
    params=[
        pytest.param((index, subsection), id=subsection.identifier)
        for section in doctypes.SECTIONS
        for index, subsection in enumerate(section.subsections)
    ],
)
def enumerated_subsections(request):
    return request.param


def test_subsection_identifier_valid(subsection):
    assert re.match(r"[A-Z]+\.[1-9][0-9]*", subsection.identifier)
    assert subsection.identifier.startswith(subsection.parent.identifier)


def test_subsection_identifiers_strictly_increasing(enumerated_subsections):
    index, subsection = enumerated_subsections
    assert subsection.identifier.split(".")[-1] == str(index + 1)


def test_subsection_isnt_rule(subsection):
    assert not (
        subsection.header_text.startswith(" ✔️ **DO**")
        or subsection.header_text.startswith(" ✔️ **CONSIDER**")
        or subsection.header_text.startswith(" ❌ **AVOID**")
        or subsection.header_text.startswith(" ❌ **DO NOT**")
    )


def test_subsection_identifier_follows_case_convention(subsection):
    header_text = subsection.header_text.lstrip()
    assert header_text[0].isupper(), "header should start with an upper-case letter"
