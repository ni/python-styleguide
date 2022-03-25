"""Provide example cases of imports that need sorting and a file that needs formatted."""
import pathlib
from os import access
from os import path
from typing import Hashable
from typing import Iterable
from typing import List

import pytest


class Foo(object):  # comment should get moved
    o = 5
    i = 1

    def __init__(self, o: Iterable[int]) -> None:
        """Test class."""
        this_method = 1

        seperator = path.sep

        has_a_lot_of_empty_lines = 2
        pass
