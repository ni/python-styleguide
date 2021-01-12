"""example of a python file with linter errors.
"""


l = 5  # noqa E741: ambiguous variable name 'l' - This suppression was auto-generated to allow focus on handling new errors

if l is None:
    print("l is None")
