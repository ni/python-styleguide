# NI Python Style Guide

![logo](docs/logo.svg)

---

<!-- @TODO: We should show you some stinkin' badges -->

Welcome to NI's internal and external Python conventions and enforcement tooling.

## Written Conventions

Our written conventions can be found at https://ni.github.io/python-styleguide/.

Their source is in [docs/Coding-Conventions.md](docs/Coding-Conventions.md).

NOTE: Using the GitHub Pages link is preferable to a GitHub `/blob` link.

## Enforcement tooling

As a tool, `ni-python-styleguide` is installed like any other script:

```bash
pip install ni-python-styleguide
```

### Linting

To lint, just run the `lint` subcommand:

```bash
ni-python-styleguide lint
# or
ni-python-styleguide lint ./dir/
# or
ni-python-styleguide lint module.py
```

The rules enforced are all rules documented in the written convention, which are marked as enforced.

### Formatting

(This section to come!)

### Editor Integration

(This section to come!)
