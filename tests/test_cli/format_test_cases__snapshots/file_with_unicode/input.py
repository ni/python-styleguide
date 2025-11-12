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


def method_with_valid_name(my_normal_param):
    """Provide with a short, valid name."""
    return 5 + 7

data =   ("device_name, supported_encodings",
    [
        ("Gerät", ["1252", "iso-8859-1", "utf-8"]),
        ("l' appareil", ["1252", "iso-8859-1", "utf-8"]),
        ("デバイス", ["932", "shift-jis", "utf-8"]),
        ("장치", ["utf-8", "euc-kr"]),
        ("设备", ["utf-8", "gbk"]),
    ],
)