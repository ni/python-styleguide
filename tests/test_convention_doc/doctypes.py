"""Useful abstraction(s) on top of the convention doc"""

import itertools
import pathlib
import re


class _RuleHeader(object):
    @classmethod
    def from_text(cls, text, *, parent=None, header_depth=1):
        header_marker = f"\\n{'#'* header_depth} \\["

        return list(
            cls(text, parent=parent)
            for text in re.findall(
                r"(" + header_marker + r".*?)(?:(?=" + header_marker + r")|$)",
                text.strip(),
                re.DOTALL,
            )
        )

    def __init__(self, text, *, parent):
        if parent:
            self.parent = parent
        self.identifier = text[text.find("[") + 1 : text.find("]")]
        self.header_text = text[text.find("]") + 1 :]
        self.body_text = text[text.find("\n") + 1 :]


class Section(_RuleHeader):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
        self.subsections = SubSection.from_text(text, parent=self, header_depth=2)


class SubSection(_RuleHeader):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)
        self.rules = Rule.from_text(text, parent=self, header_depth=3)


class Rule(_RuleHeader):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)

        self.is_automatically_enforced = self.header_text.endswith("🖥️")
        self.is_automatically_fixed = self.header_text.endswith("✨")
        self.codeblocks = re.findall(r"```(.*?)```", self.body_text)


def _get_sections():
    conventions_text = (
        pathlib.Path(__file__).absolute().parent.parent.parent
        / "docs"
        / "Coding-Conventions.md"
    ).read_text(encoding="utf-8")

    convention_rules_text = conventions_text[
        conventions_text.find("<!-- Begin Auto-ID -->") :
    ]

    return Section.from_text(convention_rules_text)


SECTIONS = _get_sections()
SUBSECTIONS = list(
    itertools.chain.from_iterable(section.subsections for section in SECTIONS)
)
RULES = list(
    itertools.chain.from_iterable(subsection.rules for subsection in SUBSECTIONS)
)
