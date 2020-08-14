import pytest

from ni_python_styleguide.__main__ import main as styleguide_main


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.filterwarnings("ignore::DeprecationWarning"))


@pytest.fixture
def styleguide(request):
    """A fixture which when executed, runs the styleguide.

    Args passed to the function are equivalent to CLI args,
    and are automatically stringified.

    The return value is whether the command succeeded or failed.

    E.g. `styleguide("lint", ".")`
    """

    def runner(*args):
        if args[0] == "lint":
            # Use default formatting instead of the colored formatting
            args = [
                *args,
                "--format",
                "default",
            ]

        with pytest.raises(SystemExit) as exc_info:
            styleguide_main(["ni_python_styleguide", *map(str, args)])

        return exc_info.value.code == 0

    return runner
