"""example of a python file with linter errors.
"""

try:
    # risky command
    raise Exception("Could not find the grail")
except:  # NOQA E722: do not use bare 'except' - This suppression was auto-generated to allow focus on handling new errors
    print("try again")
