"""example of a python file with linter errors.
"""

b = 5

if b == True:  # NOQA E712: comparison to True should be 'if cond is True:' or 'if cond:' - This suppression was auto-generated to allow focus on handling new errors
    print("B is true")
