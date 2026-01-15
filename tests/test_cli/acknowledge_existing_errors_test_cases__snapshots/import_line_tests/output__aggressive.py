"""example of a python file with linter errors.
"""

import pathlib, glob  # noqa: E401, F401 - multiple imports on one line (auto-generated noqa), 'glob' imported but unused (auto-generated noqa)
import os  # noqa: I100 - Import statements are in the wrong order. 'import os' should be before 'import pathlib, glob' (auto-generated noqa)
from os import path  # noqa: F401 - 'os.path' imported but unused (auto-generated noqa)
from os.path import *  # noqa: F403 - 'from os.path import *' used; unable to detect undefined names (auto-generated noqa)
from os.path.lorem.ipsum.dolor.sit.amet.consectetur.adipiscing.elit.sed.do.eiusmod.tempor.incididunt.ut.labore.et.dolore.magna import (  # noqa: F401 - 'os.path.lorem.ipsum.dolor.sit.amet.consectetur.adipiscing.elit.sed.do.eiusmod.tempor.incididunt.ut.labore.et.dolore.magna.lorem' imported but unused (auto-generated noqa)
    aliqua,
    dolor,
    ipsum,
    lorem,
)

aliqua()
aliqua()
ipsum()
dolor()

listdir()  # noqa: F405 - 'listdir' may be undefined, or defined from star imports: os.path (auto-generated noqa)

os.listdir()


def _test_os_name():
    for (
        os  # noqa: F402 - import 'os' from line 5 shadowed by loop variable (auto-generated noqa)
    ) in range(3):
        print(os)


import collections  # noqa: E402, F401, I100, I202 - module level import not at top of file (auto-generated noqa), 'collections' imported but unused (auto-generated noqa), Import statements are in the wrong order. 'import collections' should be before 'from os.path.lorem.ipsum.dolor.sit.amet.consectetur.adipiscing.elit.sed.do.eiusmod.tempor.incididunt.ut.labore.et.dolore.magna import aliqua, dolor, ipsum, lorem' (auto-generated noqa), Additional newline in a group of imports. 'import collections' is identified as Stdlib and 'from os.path.lorem.ipsum.dolor.sit.amet.consectetur.adipiscing.elit.sed.do.eiusmod.tempor.incididunt.ut.labore.et.dolore.magna import aliqua, dolor, ipsum, lorem' is identified as Stdlib. (auto-generated noqa)
