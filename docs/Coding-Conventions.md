NOTE: This guide is a Work In Progress!

![logo](logo.svg)

<!-- TOC -->

# Purpose of coding conventions

Coding conventions serve the following purposes:

- They create a consistent look to the code, so that readers can focus on content, not layout.
- They enable readers to understand the code more quickly by making assumptions based on previous experience.
- They facilitate copying, changing, and maintaining the code.
- They demonstrate best practices.

This is a living document that represents our coding conventions. Rules that are outlined in this document are set and are not expected to change. New rules may be added over time.

# How to Read This Document

> ✔️ **DO** - a rule that should always be followed.
>
> ✔️ **CONSIDER** - a rule that should generally be followed, but can be disregarded if you fully understand the reasoning behind the rule and have a good reason not to follow it.
>
> ❌ **AVOID** - a rule indicating something is generally not a good idea, but there are known cases where breaking the rule makes sense.
>
> ❌ **DO NOT** - a rule that indicates something you should almost never do.

Additionally rules might be suffixed with one of the below:

> 💻 - The convention is automatically enforced by `ni-python-styleguide` (By running `ni-python-styleguide lint ...`)
>
> ✨ - The convention is automatically fixed by `ni-python-stylgeuide` (`ni-python-styleguide` command doesn't exist yet)

# This vs. other guides (like PEPs)

This document serves as the single source of truth when it comes to Python coding conventions for NI code. Therefore other guides (such as the Google Python styleguide or various PEP-guides) are superseded by this one.

In all cases where a convention comes from a PEP, it will be marked as such.

# This vs. `ni-python-styleguide`

Ideally, the conventions in this document would completely match the things `ni-python-styleguide` enforces.
However, some checks we enforce don't correspond to conventions here as they either represent specific syntax issues or logic errors. We assume the Python file is free from both for the purposes of this document.

## Guides considered

- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)

# Python versions

This document is applicable to all Python versions which are not end-of-life.

---

<!-- Begin Auto-ID -->

# [F] Formatting

## [F.1] General

### [F.1.1] ✔️ **DO** Use `black` to format your code 💻

> 💻 This rule is enforced by error code BLK100

`black`'s style is well-documented and can be found [here](https://black.readthedocs.io/en/stable/the_black_code_style.html).

#### Why do we need a formatter?

Honestly, there's no mechanical reason to need one. Some argue that as long as linters catch issues (bugs or style violations) then the humans can make sure the code looks readable.
This might be true for a single project, but when you consider dozens of projects with dozens of contributors, **consistency matters**.
A formatter, enforced across all of our code, ensures that a person working on project A can work on Project B without needing to spend time familiarizing himself/herself with different style.

#### Why `black`?

- `black` has virtually no configuration support:
  - If we have to choose a formatter, choosing one with virtually no configuration is generally well received, as no one gets to argue about style
  - Choosing a formatter with virtually no configuration means formatted code from one location looks the same as another location, without having to share/duplicate a config
- It is under the umbrella of the [Python Software Foundation](https://www.python.org/psf/), which is a good endorsement from the community
- It does not modify the AST of the program :tada:

### [F.1.2] ✔️ **DO** Limit your lines to a maximum length of 100 characters 💻

> 💻 This rule is enforced by error code BLK100, W505

ℹ️ This is easily managed by `black` by setting `line-length = 100` in your `pyproject.toml` under `[tool.black]` section

There is no one-size-fits-all when it comes to a maximum line length. Too short and
developers start contorting their code to fit the restriction. Too long and lines exceed
what is visible in most common tools (code editors, diff visualizers, etc...). Additionally,
automatic formatting can reduce the burden of maintaining a maximum line length, but can
also be eager in enforcing it. In the end, choosing a maximum line length isn't about
optimization, but is rather about finding a middle-ground that developers can agree on.

We have chosen 100 characters because to some developers 80/88 characters is too limiting,
and to others 110/120 is too long.

```python
# Bad - will produce BLK100
line_with_101_chars = "spaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaam"
```

```python
# Bad - will produce W505
# Also applies to looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong comments
```

```python
# Good
line_with_99_chars = "spaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaam"
# Also applies to loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong comments
```

## [F.2] Line Spacing

### [F.2.1] ✔️ **DO** Use blank lines in functions, sparingly, to indicate logical sections.

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad - no spaces to form logical breaks in code
def visit_argument_room(self, duration):
    start = datetime.now()
    while (datetime.now() - start) < duration:
        reply = self.argue_about_answer()
        if reply == "no it isn't":
            self.accuse_contradiction()
            self.define_argument()
    new_duration = self.pay_for_more_time()
    new_start = datetime.now()
    while (datetime.now() - new_start) < new_duration:
        self.argue_about_paying()
```

```python
# Good - use blank lines to separate code into logically-related sections
def visit_argument_room(self, duration):
    start = datetime.now()

    while (datetime.now() - start) < duration:
        reply = self.argue_about_answer()

        if reply == "no it isn't":
            self.accuse_contradiction()
            self.define_argument()

    new_duration = self.pay_for_more_time()
    new_start = datetime.now()

    while (datetime.now() - new_start) < new_duration:
        self.argue_about_paying()
```

```python
# Best - extract logic into well-named methods
def visit_argument_room(self, duration):
    exit_reason = self._argue_about("answer", duration=duration)

    if exit_reason == "timeout":
        new_duration = self._purchase_more_time()
        self._argue_about("purchasing", duration=new_duration)
```

---

# [N] Naming

## [N.1] Identifiers

### [N.1.1] ✔️ **DO** Use ASCII characters for all identifiers

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
møøse_costumes = "Siggi Churchill"
```

### [N.1.2] ✔️ **DO** Use a trailing underscore to avoid a name clash with a reserved keyword

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

❗️ In most situations, a _better_ name for the identifier is the solution. This rule only applies for cases where the keyword is the best name (I.e. referencing the built-in operation/element, like [`operator.and_`](https://docs.python.org/3.4/library/operator.html#operator.and_))

Examples:

- in\_
- for\_
- class\_
- input\_
- file\_

### [N.1.3] ❌ **DO NOT** Use the characters 'l' (lowercase letter el), 'O' (uppercase letter oh), or 'I' (uppercase letter eye) as single character variable names 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error codes E741, E742, E743

```python
# Bad
for l in lines:
    print(l)


class I:
    pass


class O:
    pass
```

```python
# Good
for line in lines:
    print(line)


class Inputs:
    pass


class Outputs:
    pass
```

## [N.2] Casing

### [N.2.1] ✔️ **DO** Use short, all-lowercase package and module names (Underscores are permissible, but should be avoided)

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

E.g. `tempfile` is preferred over `temp_file` or `temporary_file`

### [N.2.2] ✔️ **DO** Use `snake_case` for function, variable, and parameter names

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [N.2.3] ✔️ **DO** Use CamelCase for class names

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception is made for classes which are used primarily as a callable. They should use function naming conventions instead.

```python
# Bad
class cheese_shop:
    pass
```

```python
# Good
class CheeseShop:
    pass
```

### [N.2.4] ✔️ **DO** Use `CamelCase` for type variable names

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
from typing import TypeVar

flying_circus = TypeVar("flying_circus")
```

```python
# Good
from typing import TypeVar

FlyingCircus = TypeVar("FlyingCircus")
```

### [N.2.5] ✔️ **DO** Suffix covariant and contravariant type variables with `_co` and `_contra` respectively

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Good
from typing import TypeVar

FlyingCircus_co = TypeVar("FlyingCircus_co", covariant=True)
FlyingCircus_contra = TypeVar("FlyingCircus_contra", contravariant=True)
```

### [N.2.6] ✔️ **DO** Suffix error exceptions with "Error"

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [N.2.7] ✔️ **DO** Use `self` as the first argument to instance methods

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [N.2.8] ✔️ **DO** Use `cls` as the first argument to class methods

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [N.2.9] ✔️ **DO** Use one leading underscore only for non-public methods and instance variables

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [N.2.10] ✔️ **DO** Use `SCREAMING_CASE` for module level constants

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [N.2.11] ✔️ **CONSIDER** Using two leading underscores for truly private attributes when defining a base class

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

ℹ️ This invokes Python's name mangling which does have well-known, yet unintended side-effects. See [the docs](https://docs.python.org/3.6/tutorial/classes.html#private-variables)

---

# [L] Language Features

## [L.1] Comparisons

### [L.1.1] ✔️ **DO** Use `is` or `is not` when comparing against a singleton (like `None`) 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code E711

```python
# Bad
if cheese == None:
    pass
```

```python
# Good
if cheese is None:
    pass
```

### [L.1.2] ✔️ **DO** Use `isinstance` instead of comparing types directly 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code E721

```python
# Bad
if type(num_cheeses) is type(1):
    buy(num_cheeses)
```

```python
# Good
if isinstance(num_cheeses, int):
    buy(num_cheeses)
```

### [L.1.3] ✔️ **DO** Use the conversion to boolean to check for empty sequences

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> ‼️ Keep in mind that `None` also converts to `False`. Take care when dealing with `Optional` sequences.

```python
# Bad
if len(seq):
    pass
if not len(seq):
    pass
```

```python
# Good
if seq:
    pass
if not seq:
    pass
```

### [L.1.4] ✔️ **DO** Use the `not in` expression to test for membership 💻

> 💻 This rule is enforced by error code E713

```python
# Bad
if not cheese in cheese_list:
    complain()
```

```python
# Good
if cheese not in cheese_list:
    complain()
```

### [L.1.5] ✔️ **DO** Use the `is not` expression to test for identity 💻

> 💻 This rule is enforced by error code E714

```python
# Bad
if not cheese is None:
    buy(cheese)
```

```python
# Good
if cheese is not None:
    buy(cheese)
```

## [L.2] Lambdas

### [L.2.1] ❌ **DO NOT** Assign a lambda expression directly to an identifier 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code E731

```python
# Bad
respond = lambda: "is not"
```

```python
# Good
def respond():
    return "is not"
```

## [L.3] Exceptions

### [L.3.1] ✔️ **DO** Derive exceptions from `Exception`

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception is made for exceptions which aren't meant to be caught, in which case `BaseException` must be derived from. This should be extremely rare.

### [L.3.2] ✔️ **DO** Chain exceptions appropriately

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

When re-rasing an exception from an exception block, prefer `raise` over `raise x`.

When raising a new exception from an exception block, prefer `raise X from Y` (as this doesn't lose the original traceback).

When deliberately replacing an inner exception (`raise X from None`), ensure that relevant details are transferred to the new exception.

### [L.3.3] ✔️ **DO** Provide an exception type when catching exceptions 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code E722

Additionally, be as specific as possible.

```python
# Bad
try:
    pass
except:
    pass
```

```python
# Good
try:
    pass
except Exception:
    pass
```

```python
# Best
try:
    pass
except ImportError:
    pass
```

### [L.3.4] ✔️ **DO** Limit the body of the try block to the absolute minimum amount of code necessary to cause the possible exception

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def lunchtime():
    try:
        # Too broad!
        return eat(spam[key])
    except KeyError:
        # Will also catch KeyError raised by eat()
        return key_not_found(key)
```

```python
# Good
def lunchtime():
    try:
        value = spam[key]
    except KeyError:
        return key_not_found(key)
    else:
        return eat(value)
```

### [L.3.5] ❌ **DO NOT** Use flow control statements (`return`/`break`/`continue`) within the `finally` suite of a `try...finally`, where control flow would jump outside the `finally` suite

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

This will result in the implicit cancellation of the active exception.

```python
# Bad
def foo():
    try:
        ask_again_if_theres_any_cheese()
    finally:
        return shoot()
```

## [L.4] Context Managers

### [L.4.1] ✔️ **DO** Invoke context managers through a special function when doing something other than handling resources

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
# Doesn't signify anything other than opening/closing is happening
with connection:
    do_stuff_in_transaction(connection)
```

```python
# Good
with connection.begin_transaction():
    do_stuff_in_transaction(connection)
```

## [L.5] Return Statements

### [L.5.1] ❌ **DO NOT** Rely on the implicit `return None` if a function is expected to return a value

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def get_stock(cheese_kind):
    if in_stock(cheese_kind):
        return get_quantity(cheese_kind)
```

```python
# Good
def get_stock(cheese_kind):
    if in_stock(cheese_kind):
        return get_quantity(cheese_kind)
    return None
```

### [L.5.2] ❌ **DO NOT** Rely on the implicit `return` implictly returning `None` if a function is expected to return a value

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def get_stock(cheese_kind):
    if not in_stock(cheese_kind):
        return
    return get_quantity(cheese_kind)
```

```python
# Good
def get_stock(cheese_kind):
    if not in_stock(cheese_kind):
        return None
    return get_quantity(cheese_kind)
```

## [L.6] Strings

### [L.6.1] ✔️ **DO** Use `startswith` and `endswith` instead of slicing or indexing a string

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
if title[:4] == "King":
    pass
if title[-1] == "s":
    pass
```

```python
# Good
if title.startswith("King"):
    pass
if title.endswith("s"):
    pass
```

## [L.7] Modules

### [L.7.1] ✔️ **DO** Document a module's public API with `__all__`

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

This includes setting `__all__` to the empty list if your module has no public API.

```python
# Good
__all__ = ["spam", "ham", "eggs"]


def spam():
    pass


def ham():
    pass


def eggs():
    pass
```

```python
# Good
__all__ = []
```

### [L.7.2] ✔️ **DO** Prefix internal interfaces with a single leading underscore

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

This includes packages, modules, classes, functions, attributes and other names.

---

# [O] Code Organization

## [O.1] Imports

### [O.1.1] ✔️ **DO** Put module imports on separate lines 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code E401

```python
# Bad
import sys, os
```

```python
# Good
import os
import sys
```

### [O.1.2] ✔️ **DO** Put imports at the top of the file 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code E402

Imports come _after_ module comments and docstrings and _before_ module globals and constants.

```python
# Bad
"""Module Docstring."""
URL = "http://python.org"

import ministry
```

```python
# Good
"""Module Docstring."""

import ministry

URL = "http://python.org"
```

### [O.1.3] ✔️ **DO** Group imports by standard library, third party, then first_party

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

Additionally, you should put a blank line between each group of imports.

```python
# Bad
import my_app.utils
import os
import ministry
```

```python
# Good
import os

import ministry

import my_app.utils
```

### [O.1.4] ✔️ **DO** Use absolute imports

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception can be made for `__init__.py` files republishing child module declarations

```python
# Bad
from .sibling import rivalry
```

```python
# Good
from my_app.relationships.sibling import rivalry
```

### [O.1.5] ❌ **DO NOT** Use wildcard imports 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

> 💻 This rule is enforced by error code F403

ℹ️ An exception can be made if you are overwriting an internal interface and you do not know which definitions will be overwritten

```python
# Bad - Pollutes the namespace
from ministry import *
```

```python
# Good - Doesn't pollute, but usage might still be confusing
from ministry import silly_walk
```

```python
# Best - Doesn't pollute and usage won't confuse
import ministry
```

### [O.1.6] ❌ **DO NOT** Rely on a module's imported names

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

ℹ️ Exceptions are made for:

- Explicitly documented cases (E.g. `os.path`)
- Names in a module's `__init__.py`

```python
# Bad
# cheese_shop.py - Imports module `brie`
import brie

# customer.py - Relying on the fact that `cheese_shop` imported module `brie`
import cheese_shop.brie
```

### [O.1.7] ❌ **DO NOT** Import definitions that are not used 💻

> 💻 This rule is enforced by error code F401

```python
# Bad
import os  # Assuming os is never used
```

## [O.2] Declarations

### [O.2.1] ❌ **DO NOT** Redefine or "shadow" declarations 💻

> 💻 This rule is enforced by error codes F402, F811

```python
# Bad - Will produce F402
import cheese

for cheese in ["Caithness", "Sage Derby", "Gorgonzola"]:
    pass
```

```python
# Bad - Will produce F811
def eat_lunch():
    pass


def eat_lunch():
    pass
```

### [O.2.2] ❌ **DO NOT** Declare unused variables 💻

> 💻 This rule is enforced by error codes F841

If a variable must exist but won't be used it is permissible to name the variable a single underscore `_`.

```python
# Bad
def purchase_cheese():
    cheese = "Gorgonzola"
```

```python
# Bad
def feast_upon():
    first, *skip_a_bit, last = ["lambs", "sloths", "breakfast cereals", "fruit bats"]
    return [first, last]
```

```python
# Good
def feast_upon():
    first, *_, last = ["lambs", "sloths", "breakfast cereals", "fruit bats"]
    return [first, last]
```

### [O.2.3] ✔️ **DO** Put module level dunder names after module docstring and before import statements

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Good
"""Lumberjack: Cuts down trees, among other things."""

__all__ = ["cut_down_trees", "eat_lunch", "go_shopping"]
__version__ = "0.1"

import os
import sys


def cut_down_trees():
    pass


def eat_lunch():
    pass


def go_shopping():
    pass
```

---

# [D] Documentation

## [D.1] Docstrings

### [D.1.1] ✔️ **DO** Write docstrings for all public packages, modules, functions, classes, and methods 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008) and [PEP 257](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring)

> 💻 This rule is enforced by error codes D100-D107

ℹ️ You can document a package by documenting the module docstring of the package directory's `__init__.py`

### [D.1.2] ✔️ **DO** List exported modules and subpackages in a package's docstring

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

### [D.1.3] ✔️ **DO** List relevant exported objects (classes, functions, exceptions, etc...) in a module's docstring

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

Each documented object should have a one-line summary (with less detail than the summary line of the objects' docstring)

### [D.1.4] ✔️ **DO** Fully document a function in its docstring

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

This includes (if applicable) the function's:

- arguments (including optional arguments, and keyword arguments)
- return value
- side effects
- possible exceptions raised
- restrictions on usage

### [D.1.5] ✔️ **DO** Fully document a class in its docstring

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

ℹ️ See the [Google docstring conventions for classes](https://google.github.io/styleguide/pyguide.html#384-classes)

This includes (if applicable) the class's:

- overall behavior
- public methods
- public instance variables
- additional info for subclasses

It should not include the specific documentation for the constructor or methods.

### [D.1.6] ✔️ **DO** Fully document a class's constructor and public methods

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

These should follow the guidance on function docstrings.

Note that the class's constructor doesn't need to document the instance variables, as that should be
covered by the class's docstring.

### [D.1.7] ✔️ **DO** Document a subclass (even if its behavior is mostly inherited)

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

When documenting a subclass, mention the differences from superclass behavior. Additionally:

- Use the verb "override" to indicate that a subclass method replaces a superclass method and does not call the superclass method.
- Use the verb "extend" to indicate that a subclass method calls the superclass method (in addition to its own behavior)

### [D.1.8] ✔️ **DO** Use complete, grammatically correct sentences, ended with a period 💻

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

> 💻 This rule is enforced by error codes D415

```python
# Bad - missing a period at the end
class CheeseShop(object):
    """Finest cheese shop in the district, offering a wide variety of cheeses"""
```

```python
# Good
class CheeseShop(object):
    """Finest cheese shop in the district, offering a wide variety of cheeses."""
```

### [D.1.9] ✔️ **DO** Write your docstrings as a command

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

E.g. "Do this", "Return that" instead of "Returns the ...".

### [D.1.10] ✔️ **DO** Start multiline docstrings with a one-line summary followed by a blank line 💻

> 💻 This rule is enforced by error codes D205, D212

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

The summary line should be on the same line as the opening quotes.

```python
# Bad - will produce D205
def sell(type_):
    """Sell the specified type of cheese.
    Will throw an OutOfStockException if the specified type of cheese is out of stock.
    """
```

```python
# Bad - will produce D212
def sell(type_):
    """
    Sell the specified type of cheese.

    Will throw an OutOfStockException if the specified type of cheese is out of stock.
    """
```

```python
# Good
def sell(type_):
    """Sell the specified type of cheese.

    Will throw an OutOfStockException if the specified type of cheese is out of stock.
    """
```

```python
# Good
class CheeseShop(object):
    """Finest cheese shop in the district, offering a wide variety of cheeses."""

    def sell(self, type_):
        """Sell the specified type of cheese."""
```

### [D.1.11] ✔️ **DO** Put closing `"""` on its own line for multiline docstrings 💻

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008) and [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

> 💻 This rule is enforced by error code D209

```python
# Bad
class CheeseShop(object):
    """Finest cheese shop in the district, offering a wide variety of cheeses.

    Cheeses are sold first-come-first-served, and can run out of stock rather quickly."""

    def sell(self, type_):
        """Sell the specified type of cheese.

        Will throw an OutOfStockException if the specified type of cheese is out of stock."""
```

```python
# Good
class CheeseShop(object):
    """Finest cheese shop in the district, offering a wide variety of cheeses.

    Cheeses are sold first-come-first-served, and can run out of stock rather quickly.
    """

    def sell(self, type_):
        """Sell the specified type of cheese.

        Will throw an OutOfStockException if the specified type of cheese is out of stock.
        """
```

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

### [D.1.12] ❌ **DO NOT** Put a blank line before a docstring 💻

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

> 💻 This rule is enforced by error codes D201, D211

```python
# Bad - will produce D211
class CheeseShop(object):

    """Finest cheese shop in the district, offering a wide variety of cheeses."""
```

```python
# Bad - will produce D201
class CheeseShop(object):
    def sell(self, type_):

        """Sell the specified type of cheese."""
```

```python
# Good
class CheeseShop(object):
    """Finest cheese shop in the district, offering a wide variety of cheeses."""

    def sell(self, type_):
        """Sell the specified type of cheese."""
```

### [D.1.13] ❌ **DO NOT** Put a blank line after a one line function docstring 💻

> 🐍 This rule stems from [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

> 💻 This rule is enforced by error code D202

```python
# Bad
def sell(self, type_):
    """Sell the specified type of cheese."""

    self._do_transaction(type_)
```

```python
# Good
def sell(self, type_):
    """Sell the specified type of cheese."""
    self._do_transaction(type_)
```

---

# [C] Comments

## [C.1] All Comments

### [C.1.1] ✔️ **DO** Use complete sentences (with periods for multiple sentences)

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [C.1.2] ✔️ **DO** Capitalize the first word, unless it is an identifier that begins with a lower case letter

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [C.1.3] ✔️ **DO** Start comments with a `#` and a single space (unless otherwise stated)

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

## [C.2] Block Comments

### [C.2.1] ✔️ **DO** Indent block comments to the same level as the code

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [C.2.2] ✔️ **DO** Start each line of a block comment with a `#` and a single space (unless it is indented text inside the comment)

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [C.2.3] ✔️ **DO** Separate paragraphs inside a block comment by a line containing a single `#`

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

## [C.3] Inline Comments

### [C.3.1] ✔️ **CONSIDER** Using inline comments sparingly

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [C.3.2] ✔️ **DO** Separate statements and inline comments by two spaces

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Good
order = ["egg", "sausage", "bacon"]  # The client doesn't want any spam
```

---

# [S] Source Files/Directories

## [S.1] Encoding

### [S.1.1] ✔️ **DO** Use UTF-8 for source code

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

### [S.1.2] ❌ **DO NOT** Use an encoding declaration

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
# -*- coding: utf-8 -*-

...
```

### [S.1.3] ❌ **AVOID** Using non-ASCII characters in string literals and comments

> 🐍 This rule stems from [PEP 8](https://www.python.org/dev/peps/pep-0008)

ℹ️ Exceptions can be made for:

- Emojis, when necessary (E.g. Strings displayed to the user)
- Test code which is testing non-ASCII encoded data
- A person's name

```python
# Bad
if being_hit_on_the_head:
    raise Exception("ᕙ(⇀‸↼‶)ᕗ: Waaaaa")
```
