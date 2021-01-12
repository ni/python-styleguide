"""example of a python file with linter errors.
"""

spam = lambda: ["eggs"] + ["spam"] * 7  # noqa E731: do not assign a lambda expression, use a def - This suppression was auto-generated to allow focus on handling new errors
