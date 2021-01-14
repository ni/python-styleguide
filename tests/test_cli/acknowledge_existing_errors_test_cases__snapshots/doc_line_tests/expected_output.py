def method1():  # noqa D100: Missing docstring in public module, D103: Missing docstring in public function - This suppression was auto-generated to allow focus on handling new errors
    return 7


def method2():
    """Provide an examples of doc strings that are too long.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """  # noqa W505: doc line too long (127 > 100 characters) - This suppression was auto-generated to allow focus on handling new errors
    return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.


class Foo:  # noqa D101: Missing docstring in public class - This suppression was auto-generated to allow focus on handling new errors
    def __init__(self):  # noqa D107: Missing docstring in __init__ - This suppression was auto-generated to allow focus on handling new errors
        pass

    def add(self, o):
        """Provide an examples of doc strings that are too long.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """  # noqa W505: doc line too long (131 > 100 characters) - This suppression was auto-generated to allow focus on handling new errors
        return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.


class _PrivateFoo:
    def __init__(self):
        pass

    def add(self, o):
        """Provide an examples of doc strings that are too long.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """  # noqa W505: doc line too long (131 > 100 characters) - This suppression was auto-generated to allow focus on handling new errors
        return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
