def method1():  # noqa: D100, D103 - Missing docstring in public module (auto-generated noqa), Missing docstring in public function (auto-generated noqa)
    return 7


def method2():
    """Provide an examples of doc strings that are too long.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """  # noqa: W505 - doc line too long (127 > 100 characters) (auto-generated noqa)
    return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.


class Foo:  # noqa: D101 - Missing docstring in public class (auto-generated noqa)
    def __init__(self):  # noqa: D107 - Missing docstring in __init__ (auto-generated noqa)
        pass

    def add(self, o):
        """Provide an examples of doc strings that are too long.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """  # noqa: W505 - doc line too long (131 > 100 characters) (auto-generated noqa)
        return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.


class _PrivateFoo:
    def __init__(self):
        pass

    def add(self, o):
        """Provide an examples of doc strings that are too long.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """  # noqa: W505 - doc line too long (131 > 100 characters) (auto-generated noqa)
        return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
