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

The script name `nps` is a short-name for `ni-python-styleguide`, and may be used in place of `ni-python-styleguide` in any CLI command.

### Linting

To lint, just run the `lint` subcommand (from within the project root, or lower):

```bash
ni-python-styleguide lint
# or
ni-python-styleguide lint ./dir/
# or
nps lint module.py
```

The rules enforced are all rules documented in the written convention, which are marked as enforced.

### Configuration

`ni-python-styleguide` aims to keep the configuration to a bare minimum (none wherever possible).
However there are some situations you might need to configure the tool.

### Fix

`ni-python-styleguide` has a subcommand `fix` which will run [black](https://pypi.org/project/black/) and [isort](https://pycqa.github.io/isort/) to apply basic formatting fixes.

When using the `--aggressive` option with `fix`, it will first run `black` and `isort` to fix what it can then add acknowledgements (`# noqa`) for any remaining linting errors that cannot be automatically fixed.

#### When using `setup.py`

If you're using `setup.py`, you'll need to set your app's import names for import sorting.

```toml
# pyproject.toml
[tool.ni-python-styleguide]
application-import-names = "<app_name>"
```

### Formatting

`ni-python-styleguide` has a subcommand `format` which will run [black](https://pypi.org/project/black/) and [isort](https://pycqa.github.io/isort/) with the correct settings to match the linting expectations.

If you wish to be able to invoke black directly, you'll want to set the following to get `black` formatting as the styleguide expects.

```toml
# pyproject.toml
[tool.black]
line-length = 100
```

### Editor Integration

#### Vim/Neovim

1. Install the [ALE](https://github.com/dense-analysis/ale) plugin. This is a
   popular asynchronous lint engine for Vim and Neovim and already does most of
   the heavy lifting for us. It supports many different ways to lint and fix
   code. Check out the documentation (`:help ale`) for more information.
2. Because `ni-python-styleguide` is a wrapper around `flake8`, you can add the
   following vim configuration lines to wherever you configure your vim project
   (you can do it in your `init.vim` or `vimrc` file, but then it will apply to
   all Python code you edit):

```vim
let g:ale_python_flake8_executable = 'ni-python-styleguide'
let g:ale_python_flake8_options = 'lint'
let g:ale_linters = {'python': ['flake8']}
let g:ale_python_black_executable = 'ni-python-styleguide'
let g:ale_python_black_options = 'fix'
let g:ale_fixers = {'python': ['isort', 'black']}
```

   Note: You can set all of these with `b:` as well.

3. You can make ALE auto-fix issues, e.g., when hitting F8, or when saving:

```vim
let g:ale_fix_on_save = 1 " Fix on save
nmap <F8> <Plug>(ale_fix) " Fix on F8
```

  Change all of these to your taste.

#### VSCode


One can configure VSCode either in the [User 'settings.json' file](https://code.visualstudio.com/docs/configure/settings#_settings-json-file), or in a local [`.vscode/settings.json`](https://code.visualstudio.com/docs/configure/settings#_workspace-settingsjson-location).


1. Install the [Python extension by Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

1. Because ni-python-styleguide is a wrapper around `flake8`, you can add the following configuration
   to make it uses ni-python-styleguide's rules.

   If using Poetry:
   ```json
   "flake8.path": [
         "poetry",
         "run",
         "ni-python-styleguide",
         "lint"
      ],
   ```
   If ni-python-styleguide is directly installed
   ```json
   "flake8.path": [
         "ni-python-styleguide",
         "lint"
      ],
   ```

   (alternatively, tell `flake8` to use the ni-python-styleguide config)
   ```json
   "flake8.args": [
        "--config=.venv\\lib\\site-packages\\ni_python_styleguide\\config.ini"
   ],
   ```

1. Telling the formatter to use ni-python-styleguide's settings

   (telling VS Code to use `black` and telling `black` to use `ni-python-styleguide`'s settings file)
   ```json
   "[python]": {
        "editor.formatOnType": true,
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
   "black-formatter.args": [
      "--config=.venv\\lib\\site-packages\\ni_python_styleguide\\config.toml"
   ],
   ```

