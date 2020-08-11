"""Tests for the convention subsections"""

import re


def test_subsection_identifier_valid(subsection):
    assert re.match(r"[A-Z]+\.[1-9][0-9]*", subsection.identifier)
    assert subsection.identifier.startswith(subsection.parent.identifier)


def test_subsection_identifiers_strictly_increasing(section):
    for index, subsection in enumerate(section.subsections):
        assert subsection.identifier.split(".")[-1] == str(index + 1)


def test_subsection_isnt_rule(subsection):
    assert not (
        subsection.header_text.startswith(" ✔️ **DO**")
        or subsection.header_text.startswith(" ✔️ **CONSIDER**")
        or subsection.header_text.startswith(" ❌ **AVOID**")
        or subsection.header_text.startswith(" ❌ **DO NOT**")
    )

