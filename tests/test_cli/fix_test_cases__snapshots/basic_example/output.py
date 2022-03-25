from typing import Iterable
from typing import List
from typing import Hashable
from os import path
from os import access


class Foo(object):  # comment should get moved
    o = 5

    i = 1

    def __init__(self, o: Iterable[int]) -> None:
        this_method = 1

        serperator = path.sep

        has_a_lot_of_empty_lines = 2
        pass
