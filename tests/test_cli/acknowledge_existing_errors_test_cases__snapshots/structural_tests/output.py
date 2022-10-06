"""example of a python file with linter errors in flow and structure of code.
"""


l = 5  # noqa E741: ambiguous variable name 'l' (auto-generated noqa)
y = False

if l is None:
    x = 3
    print("l is None")

if l is None:
    print("l is None")

if y == False:  # noqa E712: comparison to False should be 'if cond is False:' or 'if not cond:' (auto-generated noqa)
    print("l is False")

if y == True:  # noqa E712: comparison to True should be 'if cond is True:' or 'if cond:' (auto-generated noqa)
    print("l is True")

if x < 5:
    print("x < 5")


def foo():  # noqa D103: Missing docstring in public function (auto-generated noqa)
    for l in range(3):  # noqa E741: ambiguous variable name 'l' (auto-generated noqa)
        pass


breakfast = lambda: ["eggs"] + ["spam"] * 7  # noqa E731: do not assign a lambda expression, use a def (auto-generated noqa)


def menu():  # noqa D103: Missing docstring in public function (auto-generated noqa)
    lunch = lambda: ["ham"] + ["corned beef"] * 7  # noqa E731: do not assign a lambda expression, use a def (auto-generated noqa)
    return breakfast, lunch


try:
    raise NotImplemented  # noqa F901: 'raise NotImplemented' should be 'raise NotImplementedError' (auto-generated noqa)
except:  # noqa E722: do not use bare 'except' (auto-generated noqa)
    pass


class Cheese_Shop:  # noqa D101: Missing docstring in public class (auto-generated noqa)  # noqa N801: class name 'Cheese_Shop' should use CapWords convention (auto-generated noqa)
    def RequestCheese(self):  # noqa N802: function name 'RequestCheese' should be lowercase (auto-generated noqa)
        """Provide method with bad name."""
        pass

    def return_no_cheese_found(self):
        """Provide method with functional lint errors."""
        cheese_found = lambda o: False  # noqa E731: do not assign a lambda expression, use a def (auto-generated noqa)

        try:
            raise NotImplemented  # noqa F901: 'raise NotImplemented' should be 'raise NotImplementedError' (auto-generated noqa)
        except:  # noqa E722: do not use bare 'except' (auto-generated noqa)
            pass

        l = 5  # noqa E741: ambiguous variable name 'l' (auto-generated noqa)
        i = 3  # noqa F841: local variable 'i' is assigned to but never used (auto-generated noqa)

        if l == True:  # noqa E741: ambiguous variable name 'l' (auto-generated noqa)  # noqa E712: comparison to True should be 'if cond is True:' or 'if cond:' (auto-generated noqa)
            return False

        return cheese_found
