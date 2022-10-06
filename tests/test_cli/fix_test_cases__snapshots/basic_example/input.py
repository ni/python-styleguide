"""Provide example cases of imports that need sorting and a file that needs formatted."""
from typing import (
    Iterable,
    List,
    Hashable,  # noqa F401: un-used import comment that is actually used, should get removed in --aggressive (auto-generated noqa)
)
import pytest
import pathlib
from os import path, access

"""
imports in multiline strings are left alone
>>> import foo, bar
import beef, chicken
"""


class Foo(object):  # comment should get moved
    """Provide dummy code."""

    o = 5
    i = 1

    def __init__(self, o: Iterable[int]) -> None:
        """Test class."""
        this_method = 1

        self.seperator = path.sep * this_method

        pass

    @pytest.mark.skip(reason="not a test")
    def method_to_use_everything(self, x: Iterable[List[Hashable]], p: pathlib.Path):
        "Strange method."
        x = access(p)
        return x
