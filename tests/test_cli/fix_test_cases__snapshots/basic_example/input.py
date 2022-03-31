"""Provide example cases of imports that need sorting and a file that needs formatted."""
from typing import Iterable, List, Hashable
import pytest
import pathlib
from os import path, access

"""
imports in multiline strings are left alone
>>> import foo, bar
import beef, chicken
"""


class Foo(object):  # comment should get moved
    o = 5
    i = 1

    def __init__(self, o: Iterable[int]) -> None:
        """Test class."""
        this_method = 1

        seperator = path.sep

        has_a_lot_of_empty_lines = 2
        pass
