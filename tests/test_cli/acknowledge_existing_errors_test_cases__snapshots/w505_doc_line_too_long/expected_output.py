"""example of a python file with linter errors.
"""


def method():
    """Provide an examples of doc strings that are too long.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """  # noqa W505: doc line too long (127 > 100 characters) - This suppression was auto-generated to allow focus on handling new errors
    return 7  # Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
