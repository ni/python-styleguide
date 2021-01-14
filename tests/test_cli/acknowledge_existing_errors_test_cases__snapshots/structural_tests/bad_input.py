"""example of a python file with linter errors in flow and structure of code.
"""


l = 5
y = False

if l is None:
    x = 3
    print("l is None")

if l is None:
    print("l is None")

if y == False:
    print("l is False")

if y == True:
    print("l is True")

if x < 5:
    print("x < 5")

def foo():
    for l in range(3):
        pass


breakfast = lambda: ["eggs"] + ["spam"] * 7


def menu():
    lunch = lambda: ["ham"] + ["corned beef"] * 7
    return breakfast, lunch


try:
    raise NotImplemented
except:
    pass


class Cheese_Shop:
    def RequestCheese(self):
        """Provide method with bad name."""
        pass

    def return_no_cheese_found(self):
        """Provide method with functional lint errors."""
        cheese_found = lambda o: False

        try:
            raise NotImplemented
        except:
            pass

        l = 5
        i = 3

        if l == True:
            return False

        return cheese_found
