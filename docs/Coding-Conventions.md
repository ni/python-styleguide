NOTE: This guide is a Work In Progress!

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

> 💻 - The convention is automatically enforced through tooling (I.e lint error)
>
> ✨ - The convention is automatically fixed through tooling

# This vs. other guides (like PEPs)

This document serves as the single source of truth when it comes to Python coding conventions for NI code. Therefore other guides (such as the Google Python styleguide or various PEP-guides) are superseded by this one.

We have consciously decided to extract conventions from existing guides, instead of simply linking to them to minimize the scattering of conventions, to mirror other language conventions, as well as to allow us to tweak the conventions where necessary.

In all cases where a convention comes from a PEP, it will be marked as such.

## Guides considered

- [PEP-8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

---

<!-- Begin Auto-ID -->

# [F] Formatting

## [F.1] Indents

### [F.1.1] ✔️ **DO** Use 4 spaces per indentation level (never tabs)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

## [F.2] Line Spacing

### [F.2.1] ✔️ **DO** Use a line break before a binary operator

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

This not only matches mathematical publications, but also results in more readable code:

```python
# Bad
directors = (
    specially_trained_ecuradorian_mountain_llamas +
    venezuelan_red_llamas +
    mexican_whooping_llamas +
    north_chilean_guanacos +
    reg_llama_of_brixton +
    battery_llamas +
    (terry_gilliam & terry_jones)
)

# Good
directors = (
    specially_trained_ecuradorian_mountain_llamas
    + venezuelan_red_llamas
    + mexican_whooping_llamas
    + north_chilean_guanacos
    + reg_llama_of_brixton
    + battery_llamas
    + (terry_gilliam & terry_jones)
)
```

### [F.2.2] ✔️ **DO** Surround top-level function and class definitions with two blank lines

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [F.2.3] ✔️ **DO** Surround method definitions inside a class by a single blank line

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [F.2.4] ✔️ **DO** Use blank lines in functions, sparingly, to indicate logical sections.

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad - no spaces to form logical breaks in code
def visit_argument_room(duration):
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

# Good - use blank lines to separate code into logically-related sections
def visit_argument_room(duration):
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

# Best - extract logic into well-named methods
def visit_argument_room(duration):
    exit_reason = self._argue_about("answer", duration=duration)

    if exit_reason == "timeout":
        new_duration = self._purchase_more_time()
        self._argue_about("purchasing", duration=new_duration)
```

### [F.2.4] ❌ **DO NOT** Put multiple statements on one line

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
if answer == "no it isn't": accuse_contradiction()

define_argument(); pay_for_more_time(); argue_about_paying()

# Good
if answer == "no it isn't":
    accuse_contradiction()

define_argument()
pay_for_more_time()
argue_about_paying()
```

## [F.3] Character Spacing

### [F.3.1] ❌ **DO NOT** Use whitespace immediately inside parentheses, brackets or braces

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
spam( ham[ 1 ], { eggs: 2 } )

# Good
spam(ham[1], {eggs: 2})
```

### [F.3.2] ❌ **DO NOT** Use whitespace between a trailing comma and a following close parenthesis

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
spam = (0, )

# Good
spam = (0,)
```

### [F.3.3] ❌ **DO NOT** Use whitespace immediately before a comma, semicolon, or colon

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception is made (and **must** be followed) for situations where the colon is acting like a binary operator and other operators are present. Then it **must** be surrounded by whitespace like any other operator.

```python
# Bad
if x == 4 :
    print x , y
    x , y = y , x
ham[lower + offset:upper + offset]
ham[1: 9], ham[1 :9], ham[1:9 :3]
ham[lower : : upper]
ham[ : upper]

# Good
if x == 4:
    print x, y
    x, y = y, x

ham[lower + offset : upper + offset]
ham[1:9], ham[1:9], ham[1:9:3]
ham[lower::upper]
ham[:upper]
```

### [F.3.4] ❌ **DO NOT** Use whitespace immediately before the open parenthesis that starts the argument list of a function call

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
spam (1)

# Good
spam(1)
```

### [F.3.5] ❌ **DO NOT** Use whitespace immediately before the open parenthesis that starts an indexing or slicing

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
spam ['bacon'] = ham [index]

# Good
spam['bacon'] = ham[index]
```

### [F.3.6] ❌ **DO NOT** Use trailing whitespace anywhere

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [F.3.7] ✔️ **DO** Surround binary operators with exactly one space on either side (unless otherwise stated)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ Rules [F.3.9] and [F.3.10] specify exceptions to this rule

```python
# Bad
order =       egg&bacon
other_order = egg&bacon&spam

# Good
order = egg & bacon
other_order = egg & bacon & spam
```

### [F.3.8] ✔️ **CONSIDER** Surrounding expressions with parenthesis when different operators are used

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
order = (spam+bacon) & (sausage+spam)
order = spam + bacon & sausage + spam

# Good
order = (spam + bacon) & (sausage + spam)
```

### [F.3.9] ❌ **DO NOT** Surround the "`=`" with spaces when used to indicate a keyword argument, or when used to indicate a default value for an _unannotated_ function parameter

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def argue(room, minutes = 5):
    return impl(r = room, m = minutes)

# Good
def argue(room, minutes=5):
    return impl(r=room, m=minutes)
```

### [F.3.10] ✔️ **DO** Surround the "`=`" with spaces when used to indicate a default value for an _annotated_ function parameter

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def argue(duration: datetime.timedelta=5): ...

# Good
def argue(duration: datetime.timedelta = 5): ...
```

## [F.4] Trailing Commas

### [F.4.1] ✔️ **DO** Parenthesize one-element tuples

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
ingredients = spam,

# Good
ingredients = (spam,)
```

### [F.4.2] ✔️ **CONSIDER** Using redundant trailing commas in collection element and argument lists

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

This can be helpful for minimizing diffs when future additions are made.

```python
feast = [
    lambs,
    sloths,
    carp,
    anchovies,
    orangutans,
    breakfast_cereals,
    fruit_bats,
]

count(
    "One!",
    "Two!",
    "Five!",
)

def count(
    first_number,
    second_number,
    third_number,
)
```

### [F.4.3] ❌ **DO NOT** Use a redundant trailing comma on the same line as a closing delimiter

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
order = [egg, sausage, bacon,]
```

## [F.5] Strings

### [F.5.1] ✔️ **DO** Use single or double quotes characters when a string contains the other character

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
movie = "\"Fillings of Passion\""
grounding = '\'O\' Level Geography'

# Good
movie = '"Fillings of Passion"'
grounding = "'O' Level Geography"

```

### [F.5.2] ✔️ **DO** Use double quotes characters for triple-quoted strings

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008) as well as [PEP-257](https://www.python.org/dev/peps/pep-0257)

```python
notice = """We apologise for the fault in the subtitles.

Those responsible have been sacked.
"""
```

---

# [N] Naming

## [N.1] Identifiers

### [N.1.1] ✔️ **DO** Use ASCII characters for all identifiers

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
møøse_costumes = "Siggi Churchill"
```

### [N.1.2] ✔️ **DO** Use a trailing underscore to avoid a name clash with a reserved keyword

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

❗️ In most situations, a _better_ name for the identifier is the solution. This rule only applies for cases where the keyword is the best name (I.e. referencing the built-in operation/element, like [`operator.and_`](https://docs.python.org/3.4/library/operator.html#operator.and_))

```python
# Acceptable
in_
for_
class_
input_
file_
```

## [N.2] Casing

### [N.2.1] ✔️ **DO** Use short, all-lowercase package and module names (Underscores are permissible, but should be avoided)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
temporary_file

# Better
temp_file

# Best
tempfile
```

### [N.2.2] ✔️ **DO** Use `snake_case` for function, variable, and parameter names

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [N.2.3] ✔️ **DO** Use CamelCase for class names

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception is made for classes which are used primarily as a callable. They should use function naming conventions instead.

```python
# Bad
class cheese_shop:
    pass

# Good
class CheeseShop:
    pass
```

### [N.2.4] ✔️ **DO** Use `CamelCase` for type variable names

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
from typing import TypeVar

# Bad
flying_circus = TypeVar("flying_circus")

# Good
FlyingCircus = TypeVar("FlyingCircus")
```

### [N.2.5] ✔️ **DO** Suffix covariant and contravariant type variables with `_co` and `_contra` respectively

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
from typing import TypeVar

FlyingCircus_co = TypeVar('FlyingCircus_co', covariant=True)
FlyingCircus_contra = TypeVar('FlyingCircus_contra', contravariant=True)
```

### [N.2.6] ✔️ **DO** Suffix error exceptions with "Error"

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [N.2.7] ✔️ **DO** Use `self` as the first argument to instance methods

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [N.2.8] ✔️ **DO** Use `cls` as the first argument to class methods

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [N.2.9] ✔️ **DO** Use one leading underscore only for non-public methods and instance variables

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [N.2.10] ✔️ **DO** Use `SCREAMING_CASE` for module level constants

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [N.2.11] ✔️ **CONSIDER** Using two leading underscores for truly private attributes when defining a base class

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ This invokes Python's name mangling which does have well-known, yet unintended side-effects. See [the docs](https://docs.python.org/3.6/tutorial/classes.html#private-variables)

---

# [L] Language Features

## [L.1] Comparisons

### [L.1.1] ✔️ **DO** Use `is` or `is not` when comparing against a singleton (like `None`)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
if cheese == None: ...

# Good
if cheese is None: ...
```

### [L.1.2] ✔️ **DO** Use `isinstance` instead of comparing types directly

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
if type(cheese) is type(that_cheese): ...

# Good
if isinstance(cheese, Gorgonzola): ...
```

### [L.1.3] ✔️ **DO** Use the conversion to boolean to check for empty sequences

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

> ‼️ Keep in mind that `None` also converts to `False`. Take care when dealing with `Optional` sequences.

```python
# Bad
if len(seq): ...
if not len(seq): ...

# Good
if seq: ...
if not seq: ...
```

## [L.2] Lambdas

### [L.2.1] ❌ **DO NOT** Assign a lambda expression directly to an identifier

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
respond = lambda: "is not"

# Good
def respond():
   return "is not"
```

## [L.3] Exceptions

### [L.3.1] ✔️ **DO** Derive exceptions from `Exception`

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception is made for exceptions which aren't meant to be caught, in which case `BaseException` must be derived from. This should be extremely rare.

### [L.3.2] ✔️ **DO** Chain exceptions appropriately

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

When re-rasing an exception from an exception block, prefer `raise` over `raise x`.

When raising a new exception from an exception block, prefer `raise X from Y` (as this doesn't lose the original traceback).

When deliberately replacing an inner exception (`raise X from None`), ensure that relevant details are transferred to the new exception.

### [L.3.3] ✔️ **DO** Provide an exception type when catching exceptions

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

Additionally, be as specific as possible.

```python
# Bad
except: ...

# Better
except Exception: ...

# Best
except ImportError: ...
```

### [L.3.4] ✔️ **DO** Limit the body of the try block to the absolute minimum amount of code necessary to cause the possible exception

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
try:
    # Too broad!
    return eat(spam[key])
except KeyError:
    # Will also catch KeyError raised by eat()
    return key_not_found(key)

# Good
try:
    value = spam[key]
except KeyError:
    return key_not_found(key)
else:
    return eat(value)
```

### [L.3.5] ❌ **DO NOT** Use flow control statements (`return`/`break`/`continue`) within the `finally` suite of a `try...finally`, where control flow would jump outside the `finally` suite

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

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

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
# Doesn't signify anything other than opening/closing is happening
with connection:
    do_stuff_in_transaction(connection)

# Good
with connection.begin_transaction():
    do_stuff_in_transaction(connection)
```

## [L.5] Return Statements

### [L.5.1] ❌ **DO NOT** rely on the implicit `return None` if a function is expected to return a value

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def get_stock(cheese_kind):
    if in_stock(cheese_kind):
        return get_quantity(cheese_kind)

# Good
def get_stock(cheese_kind):
    if in_stock(cheese_kind):
        return get_quantity(cheese_kind)
    return None
```

### [L.5.2] ❌ **DO NOT** rely on the implicit `return` implictly returning `None` if a function is expected to return a value

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
def get_stock(cheese_kind):
    if not in_stock(cheese_kind):
        return
    return get_quantity(cheese_kind)

# Good
def get_stock(cheese_kind):
    if not in_stock(cheese_kind):
        return None
    return get_quantity(cheese_kind)
```

## [L.6] Strings

### [L.6.1] ✔️ **DO** use `startswith` and `endswith` instead of slicing or indexing a string

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
if title[:4] == "King": ...
if title[-1] == "s": ...

# Good
if title.startswith("King"): ...
if title.endswith("s"): ...
```

---

# [O] Code Organization

## [O.1] Imports

### [O.1.2] ✔️ **DO** Put module imports on separate lines

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
# Bad
import sys, os

# Good
import os
import sys
```

### [O.1.2] ✔️ **DO** Put imports at the top of the file

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

Imports come _after_ module comments and docstrings and _before_ module globals and constants.

Bad:

```python
"""Module Docstring"""
URL = "http://python.org"

import ministry
```

Good:

```python
"""Module Docstring"""

import ministry

URL = "http://python.org"
```

### [O.1.3] ✔️ **DO** Group imports by standard library, third party, then first_party

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

Additionally, you should put a blank line between each group of imports.

```python
# Bad
import my_app.utils
import os
import ministry

# Good
import os

import ministry

import my_app.utils
```

### [O.1.4] ✔️ **DO** Use absolute imports

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception can be made for `__init__.py` files republishing child module declarations

```python
# Bad
from .sibling import rivalry

# Good
from my_app.relationships.sibling import rivalry
```

### [O.1.5] ❌ **DO NOT** Use wildcard imports

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ An exception can be made if you are overwriting an internal interface and you do not know which definitions will be overwritten

```python
# Bad - Pollutes the namespace
from ministry import *

# Good - Doesn't pollute, but usage might still be confusing
from ministry import silly_walk

# Best - Doesn't pollute and usage won't confuse
import ministry
```

## [O.2] Declarations

### [O.2.1] ✔️ **DO** Put module level dunder names after module docstring and before import statements

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
"""Lumberjack: Cuts down trees, among other things"""

__all__ = ["cut_down_trees", "eat_lunch", "go_shopping"]
__version__ = "0.1"

import os
import sys
```

---

# [D] Documentation

## [D.1] Docstrings

### [D.1.1] ✔️ **DO** Write docstrings for all public modules, functions, classes, and methods

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008) and [PEP 257](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring)

### [D.1.2] ✔️ **DO** Put closing `"""` on the same line for one line docstrings

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008) and [PEP 257](https://www.python.org/dev/peps/pep-0257/#one-line-docstrings)

### [D.1.3] ✔️ **DO** Put closing `"""` on its own line for multiline docstrings

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008) and [PEP 257](https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings)

---

# [C] Comments

## [C.1] All Comments

### [C.1.1] ✔️ **DO** Use complete sentences (with periods for multiple sentences)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [C.1.2] ✔️ **DO** Capitalize the first word, unless it is an identifier that begins with a lower case letter

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [C.1.3] ✔️ **DO** Start comments with a `#` and a single space (unless otherwise stated)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

## [C.2] Block Comments

### [C.2.1] ✔️ **DO** Indent block comments to the same level as the code

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [C.2.2] ✔️ **DO** Start each line of a block comment with a `#` and a single space (unless it is indented text inside the comment)

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [C.2.3] ✔️ **DO** Separate paragraphs inside a block comment by a line containing a single `#`

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

## [C.3] Inline Comments

### [C.3.1] ✔️ **CONSIDER** Using inline comments sparingly

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [C.3.2] ✔️ **DO** Separate statements and inline comments by two spaces

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

```python
order = [egg, sausage, bacon]  # The client doesn't want any spam
```

---

# [S] Source Files/Directories

## [S.1] Encoding

### [S.1.1] ✔️ **DO** Use UTF-8 for source code

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

### [S.1.2] ❌ **DO NOT** Use an encoding declaration

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

Bad:

```python
# -*- coding: utf-8 -*-

...
```

### [S.1.3] ❌ **AVOID** Using non-ASCII characters in string literals and comments

> 🐍 This rule stems from [PEP-8](https://www.python.org/dev/peps/pep-0008)

ℹ️ Exceptions can be made for:

- Emojis, when necessary (E.g. Strings displayed to the user)
- Test code which is testing non-ASCII encoded data
- A person's name

```python
# Bad
if being_hit_on_the_head:
    raise Exception("ᕙ(⇀‸↼‶)ᕗ: Waaaaa")
```
