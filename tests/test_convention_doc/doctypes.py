"""Useful abstractions on top of the convention document."""

import itertools
import pathlib
import re


class _Region(object):
    @classmethod
    def from_text(cls, text, *, parent=None, header_depth=1):
        """Return the region from the given convention text.

        `parent` is forwarded to the constructor.
        `header_depth` specifies which Markdown header depth to identify the section by.
        """
        header_marker = f"\\n{'#'* header_depth} \\["

        return list(
            cls(text.strip(), parent=parent)
            for text in re.findall(
                r"(" + header_marker + r".*?)(?:(?=" + header_marker + r")|$)",
                text.strip(),
                re.DOTALL,
            )
        )

    def __init__(self, text, *, parent=None):
        """Construct the region from the given convention text.

        `parent` can be optionally specified and should be a region which this region is a child of.
        """
        if parent:
            self.parent = parent
        self.identifier = text[text.find("[") + 1 : text.find("]")]
        self.header_text = text[text.find("]") + 1 : text.find("\n")]
        self.body_text = text[text.find("\n") + 1 :]


class Section(_Region):
    """A section in the convention document.

    Sections are the broad categories the convention encompasses (E.g. "docstrings") and are
    identified in the text by heading level 1.

    Each section's identifier should simply be alphabetic identifier (E.g. "D").
    """

    def __init__(self, text, **kwargs):
        """Construct the section.

        See help(_Region.__init__) for argument information.
        """
        super().__init__(text, **kwargs)
        self.subsections = SubSection.from_text(text, parent=self, header_depth=2)


class SubSection(_Region):
    """A subsection in the convention document.

    Subsections are the specific categories underneath a section (E.g. if the section is about
    conventions regarding language features, there might be a subsection per language feature).
    They are identified in the text by heading level 2.

    Each subsection's identifier is the section's identifier followed by a period and
    the identifying subsection number (E.g. "D.1").
    """

    def __init__(self, text, **kwargs):
        """Construct the subsection.

        See help(_Region.__init__) for argument information.
        """
        super().__init__(text, **kwargs)
        self.rules = Rule.from_text(text, parent=self, header_depth=3)


class Rule(_Region):
    """A rule in the convention document.

    Rules are the specific conventions within a subsection and are identified in the text by heading level 3.

    Each rule's identifier is the subsection's identifier followed by a period and the identifying
    rule number (E.g. "D.1.1").
    """

    def __init__(self, text, **kwargs):
        """Construct the rule.

        See help(_Region.__init__) for argument information.
        """
        super().__init__(text, **kwargs)

        self.is_automatically_enforced = self.header_text.endswith("💻")
        self.is_automatically_fixed = self.header_text.endswith("✨")
        self.codeblocks = [
            Codeblock(self, match["language"], match["description"], match["body"])
            for match in Rule._find_codeblocks(self.body_text)
        ]

    @staticmethod
    def _find_codeblocks(text):
        r"""Find codeblocks in given text, yielding match objects.

        >>> [match.groupdict() for match in Rule._find_codeblocks('```x=5```')]
        [{'language': None, 'description': None, 'body': 'x=5'}]

        >>> [match.groupdict() for match in Rule._find_codeblocks('```python\nx=5```')]
        [{'language': 'python', 'description': None, 'body': 'x=5'}]

        >>> [
        ...     match.groupdict()
        ...     for match in
        ...     Rule._find_codeblocks('```python\n# Bad\nx=5```')
        ... ]
        [{'language': 'python', 'description': 'Bad', 'body': 'x=5'}]

        >>> [match.groupdict() for match in Rule._find_codeblocks('```\n# Bad\nx=5```')]
        [{'language': None, 'description': 'Bad', 'body': 'x=5'}]

        """
        yield from re.finditer(
            r"```((?P<language>[a-z]+)\n)?(\n?# (?P<description>.*?)\n)?(?P<body>.*?)```",
            text,
            flags=re.DOTALL,
        )

    @property
    def error_codes(self):
        """Return the error codes this rule is enforced by if any, None otherwise."""
        match = re.search(r"\n> 💻 This rule is enforced by error codes? (.*?)\n", self.body_text)
        if match:
            return [error_code.strip("` ") for error_code in match[1].split(",")]
        return None


class Codeblock(object):
    """A codeblock in the convention document."""

    def __init__(self, rule, language, description, contents):
        """Construct the codeblock.

        `rule` should be the Rule this codeblock is under.
        `language` should be the programming language specified for the codeblock.
        `description` should be the description of the codeblock, (usually the first commented line)
        `contents` should be the codeblock contents.
        """
        self.rule = rule
        self.language = language
        self.descriptor = description.split()[0] if description else description
        self.contents = contents


def _get_sections():
    conventions_text = (
        pathlib.Path(__file__).absolute().parent.parent.parent / "docs" / "Coding-Conventions.md"
    ).read_text(encoding="utf-8")

    convention_rules_text = conventions_text[conventions_text.find("<!-- Begin Auto-ID -->") :]

    return Section.from_text(convention_rules_text)


SECTIONS = _get_sections()
SUBSECTIONS = list(itertools.chain.from_iterable(section.subsections for section in SECTIONS))
RULES = list(itertools.chain.from_iterable(subsection.rules for subsection in SUBSECTIONS))
