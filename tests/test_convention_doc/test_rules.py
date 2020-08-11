"""Tests for the convention rules"""

import re


def test_rule_identifier_valid(rule):
    assert re.match(r"[A-Z]+\.[1-9][0-9]*\.[1-9][0-9]*", rule.identifier)
    assert rule.identifier.startswith(rule.parent.identifier)


def test_rule_identifiers_strictly_increasing(subsection):
    for index, rule in enumerate(subsection.rules):
        assert rule.identifier.split(".")[-1] == str(index + 1)


def test_rule_identifier_follows_convention(rule):
    assert (
        rule.header_text.startswith(" ✔️ **DO**")
        or rule.header_text.startswith(" ✔️ **CONSIDER**")
        or rule.header_text.startswith(" ❌ **AVOID**")
        or rule.header_text.startswith(" ❌ **DO NOT**")
    )


def test_rule_has_at_most_one_codeblock(rule):
    assert len(rule.codeblocks) <= 1

