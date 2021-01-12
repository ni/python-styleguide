"""example of a python file with linter errors.
"""


x = 5

if x == None:  # NOQA E711: comparison to None should be 'if cond is None:' - This suppression was auto-generated to allow focus on handling new errors
    print("X is None")
