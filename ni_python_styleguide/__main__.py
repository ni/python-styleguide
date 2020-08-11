import pathlib
import sys

import ni_python_styleguide._vendor.flakehell as flakehell

_CONFIGURABLE_COMMANDS = ["baseline", "lint", "missed", "plugins"]


def main(argv=sys.argv):
    args = argv[1:]
    if args and args[0] in _CONFIGURABLE_COMMANDS:
        args.extend(
            [
                "--append-config",
                str(pathlib.Path(__file__).parent / "flakehell_config.toml"),
            ]
        )
    flakehell.entrypoint(args)


if __name__ == "__main__":
    main(sys.argv)
