"""Tests for the convention sections"""

import re


def test_section_identifier_valid(section):
    assert re.match(r"[A-Z]+", section.identifier)


def test_section_identifiers_unique(sections):
    section_identifiers = set()
    for section in sections:
        assert section.identifier not in section_identifiers
        section_identifiers.add(section.identifier)
