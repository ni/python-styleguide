# NI Python Style Guide

![logo](https://raw.githubusercontent.com/ni/python-styleguide/main/docs/logo.svg)

---

[![PyPI version](https://badge.fury.io/py/ni-python-styleguide.svg)](https://badge.fury.io/py/ni-python-styleguide) ![Publish Package](https://github.com/ni/python-styleguide/workflows/Publish%20Package/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Welcome to NI's internal and external Python conventions and enforcement tooling.

## Written Conventions

Our written conventions can be found at https://ni.github.io/python-styleguide/.

Their source is in [docs/Coding-Conventions.md](https://github.com/ni/python-styleguide/tree/main/docs/Coding-Conventions.md).

NOTE: Using the GitHub Pages link is preferable to a GitHub `/blob` link.

## Enforcement tooling

As a tool, `ni-python-styleguide` is installed like any other script:

```bash
pip install ni-python-styleguide
```

### Linting

To lint, just run the `lint` subcommand (from within the project root, or lower):

```bash
ni-python-styleguide lint
# or
ni-python-styleguide lint ./dir/
# or
ni-python-styleguide lint module.py
```

The rules enforced are all rules documented in the written convention, which are marked as enforced.

### Configuration

`ni-python-styleguide` aims to keep the configuration to a bare minimum (none wherever possible).
However there are some situations you might need to configure the tool.

#### When using `setup.py`

If you're using `setup.py`, you'll need to set your app's import names for import sorting.

```toml
# pyproject.toml
[tool.ni-python-styleguide]
application-import-names = "<app_name>"
```

### Formatting

`ni-python-styleguide` in the future will have a `format` command which we intend to fix as many lint issues as possible.

Until then you'll want to set the following to get `black` formatting as the styleguide expects.

```toml
# pyproject.toml
[tool.black]
line-length = 100
```

### Editor Integration

(This section to come!)
