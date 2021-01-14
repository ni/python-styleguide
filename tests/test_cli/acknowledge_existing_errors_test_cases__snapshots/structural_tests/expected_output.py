"""example of a python file with linter errors in flow and structure of code.
"""


l = 5  # noqa E741: ambiguous variable name 'l' - This suppression was auto-generated to allow focus on handling new errors
y = False

if l is None:
    x = 3
    print("l is None")

if l is None:
    print("l is None")

if y == False:  # noqa E712: comparison to False should be 'if cond is False:' or 'if not cond:' - This suppression was auto-generated to allow focus on handling new errors
    print("l is False")

if y == True:  # noqa E712: comparison to True should be 'if cond is True:' or 'if cond:' - This suppression was auto-generated to allow focus on handling new errors
    print("l is True")

if x < 5:
    print("x < 5")

def foo():  # noqa D103: Missing docstring in public function - This suppression was auto-generated to allow focus on handling new errors
    for l in range(3):  # noqa E741: ambiguous variable name 'l' - This suppression was auto-generated to allow focus on handling new errors
        pass


breakfast = lambda: ["eggs"] + ["spam"] * 7  # noqa E731: do not assign a lambda expression, use a def - This suppression was auto-generated to allow focus on handling new errors


def menu():  # noqa D103: Missing docstring in public function - This suppression was auto-generated to allow focus on handling new errors
    lunch = lambda: ["ham"] + ["corned beef"] * 7  # noqa E731: do not assign a lambda expression, use a def - This suppression was auto-generated to allow focus on handling new errors
    return breakfast, lunch


try:
    raise NotImplemented  # noqa F901: 'raise NotImplemented' should be 'raise NotImplementedError' - This suppression was auto-generated to allow focus on handling new errors
except:  # noqa E722: do not use bare 'except' - This suppression was auto-generated to allow focus on handling new errors
    pass


class Cheese_Shop:  # noqa D101: Missing docstring in public class - This suppression was auto-generated to allow focus on handling new errors
    def RequestCheese(self):
        """Provide method with bad name."""
        pass

    def return_no_cheese_found(self):
        """Provide method with functional lint errors."""
        cheese_found = lambda o: False  # noqa E731: do not assign a lambda expression, use a def - This suppression was auto-generated to allow focus on handling new errors

        try:
            raise NotImplemented  # noqa F901: 'raise NotImplemented' should be 'raise NotImplementedError' - This suppression was auto-generated to allow focus on handling new errors
        except:  # noqa E722: do not use bare 'except' - This suppression was auto-generated to allow focus on handling new errors
            pass

        l = 5  # noqa E741: ambiguous variable name 'l' - This suppression was auto-generated to allow focus on handling new errors
        i = 3  # noqa F841: local variable 'i' is assigned to but never used - This suppression was auto-generated to allow focus on handling new errors

        if l == True:  # noqa E741: ambiguous variable name 'l', E712: comparison to True should be 'if cond is True:' or 'if cond:' - This suppression was auto-generated to allow focus on handling new errors
            return False

        return cheese_found
