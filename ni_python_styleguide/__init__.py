"""NI's internal and external style rules enforcement tool for Python."""


class _Flake8Error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.code = args[0]
