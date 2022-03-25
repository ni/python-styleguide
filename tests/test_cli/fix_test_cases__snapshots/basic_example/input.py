from typing import Iterable, List, Hashable
from os import path, access


class Foo(object):  # comment should get moved
    o = 5
    i = 1

    def __init__(self, o: Iterable[int]) -> None:
        this_method = 1

        serperator = path.sep

        has_a_lot_of_empty_lines = 2
        pass
