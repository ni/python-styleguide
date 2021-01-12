"""example of a python file with linter errors.
"""


def spam():
    """Return the breakfast menu."""
    return ["eggs"] + ["spam"] * 7


import os.path  # NOQA E402: module level import not at top of file - This suppression was auto-generated to allow focus on handling new errors

os.path.listdir()
