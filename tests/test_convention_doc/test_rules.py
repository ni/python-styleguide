"""Tests for the convention rules."""

import re

import pytest

from tests.test_convention_doc import doctypes


@pytest.fixture(
    scope="module",
    params=[
        pytest.param((index, rule), id=rule.identifier)
        for subsection in doctypes.SUBSECTIONS
        for index, rule in enumerate(subsection.rules)
    ],
)
def enumerated_rule(request):
    """Each rule along with its index in the parent subsection."""
    return request.param


def test_rule_identifier_valid(rule):
    """Tests that the rule's identifier is a valid rule identifier and matches expectations."""
    assert re.match(r"[A-Z]+\.[1-9][0-9]*\.[1-9][0-9]*", rule.identifier)
    assert rule.identifier.startswith(rule.parent.identifier)


def test_rule_identifiers_strictly_increasing(enumerated_rule):
    """Tests that the rules in a subsection use strictly incrementing identifiers."""
    index, rule = enumerated_rule
    assert rule.identifier.split(".")[-1] == str(index + 1)


def test_rule_identifier_follows_prefix_convention(rule):
    """Tests that the rule title follows our prefix convention."""
    assert (
        rule.header_text.startswith(" ✔️ **DO**")
        or rule.header_text.startswith(" ✔️ **CONSIDER**")
        or rule.header_text.startswith(" ❌ **AVOID**")
        or rule.header_text.startswith(" ❌ **DO NOT**")
    )


def test_rule_identifier_follows_case_convention(rule):
    """Tests that the rule header starts with an uppercase letter."""
    rule_title = ("**".join(rule.header_text.split("**")[2:])).strip()
    assert rule_title[0] == rule_title[0].upper(), "header should start with an uppercase letter"


def test_rule_documents_enforcement_codes(rule):
    """Tests that if rule is marked as automatically enforced, it lists the relevant codes."""
    if rule.is_automatically_enforced:
        assert rule.error_codes is not None
    else:
        assert rule.error_codes is None, f"Rule ({rule.identifier}) is not marked as automatically enforced, but lists an error code {rule.error_codes}"
