"""Tests for the convention sections."""

import collections
import re


def test_section_identifier_valid(section):
    """Tests that the section's identifier is alphabetic."""
    assert re.match(r"[A-Z]+", section.identifier)


def test_section_identifiers_unique(sections):
    """Tests that the section's identifiers are unique."""
    section_identifier_counts = collections.defaultdict(int)
    for section in sections:
        section_identifier_counts[section.identifier] += 1

    assert all(count == 1 for count in section_identifier_counts.values())


def test_section_identifier_follows_case_convention(section):
    """Tests that the section's header starts with an uppercase letter."""
    header_text = section.header_text.lstrip()
    assert header_text[0].isupper(), "header should start with an uppercase letter"
