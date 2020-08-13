"""Tests for the convention rules"""

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
    return request.param


def test_rule_identifier_valid(rule):
    assert re.match(r"[A-Z]+\.[1-9][0-9]*\.[1-9][0-9]*", rule.identifier)
    assert rule.identifier.startswith(rule.parent.identifier)


def test_rule_identifiers_strictly_increasing(enumerated_rule):
    index, rule = enumerated_rule
    assert rule.identifier.split(".")[-1] == str(index + 1)


def test_rule_identifier_follows_prefix_convention(rule):
    assert (
        rule.header_text.startswith(" ✔️ **DO**")
        or rule.header_text.startswith(" ✔️ **CONSIDER**")
        or rule.header_text.startswith(" ❌ **AVOID**")
        or rule.header_text.startswith(" ❌ **DO NOT**")
    )


def test_rule_identifier_follows_case_convention(rule):
    rule_title = ("**".join(rule.header_text.split("**")[2:])).strip()
    assert rule_title[0] == rule_title[0].upper()


def test_rule_has_at_most_one_codeblock(rule):
    assert len(rule.codeblocks) <= 1

