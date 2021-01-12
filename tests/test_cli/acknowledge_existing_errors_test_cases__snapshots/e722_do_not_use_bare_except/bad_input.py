"""example of a python file with linter errors.
"""

try:
    # risky command
    raise Exception("Could not find the grail")
except:
    print("try again")
