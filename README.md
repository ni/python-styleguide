# NI Python Style Guide

![logo](docs/logo.svg)

---

<!-- @TODO: We should show you some stinkin' badges -->

Welcome to NI's internal and external Python conventions and linter rules/plugins/tooling.

`ni-python-styleguide` serves several purposes:

1. It is a `flake8` plugin that aggregates several other `flake8` plugins
1. It houses our approved `flakehell` config: `flakehell_config.toml`
1. When run directly, combines the above

## Written Conventions

Our written conventions can be found at https://ni.github.io/python-styleguide/.

NOTE: Using the GitHub Pages link is preferable to a GitHub `/blob` link.

## Quickstart

```bash
pip install ni-python-styleguide
```

## Running

```bash
ni-python-styleguide lint
# or
ni-python-styleguide lint ./dir/
# or
ni-python-styleguide lint module.py
```

`ni-python-styleguide` is just a wrapper around `flakehell`, adding our config to the base configs.

Additional commands/options can be found in the [`flakehell documentation`](https://flakehell.readthedocs.io/index.html)
