"""Unicode in file should not cause error (e.g., ©)."""


class Foo:
    """Example class with unicode consts."""

    def __init__(self) -> None:
        """Instantiate Foo class."""
        self._problem_chars = "π”"

    @property
    def problem_chars(self):
        """Return stored string with a unicode char."""
        return self._problem_chars


def method_withBadName_andParams(my_normal_param, myBadlyNamedParam, my_other_Bad_param):
    """Provide example where black will want to split out result."""
    return 5 + 7
