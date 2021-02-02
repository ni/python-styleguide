"""example of a python file with linter errors.
"""

import os
from os import path  # noqa F401: 'os.path' imported but unused (auto-generated noqa)
import pathlib, glob  # noqa F401: 'pathlib' imported but unused (auto-generated noqa)  # noqa E401: multiple imports on one line (auto-generated noqa)

from os.path import *  # noqa F403: 'from os.path import *' used; unable to detect undefined names (auto-generated noqa)

from os.path.lorem.ipsum.dolor.sit.amet.consectetur.adipiscing.elit.sed.do.eiusmod.tempor.incididunt.ut.labore.et.dolore.magna import (  # noqa F401: 'os.path.lorem.ipsum.dolor.sit.amet.consectetur.adipiscing.elit.sed.do.eiusmod.tempor.incididunt.ut.labore.et.dolore.magna.lorem' imported but unused (auto-generated noqa)
    aliqua,
    lorem,
    ipsum,
    dolor,
)

aliqua()
aliqua()
ipsum()
dolor()

listdir()  # noqa F405: 'listdir' may be undefined, or defined from star imports: os.path (auto-generated noqa)

os.listdir()


def _test_os_name():
    for os in range(3):  # noqa F402: import 'os' from line 4 shadowed by loop variable (auto-generated noqa)
        print(os)


import collections  # noqa E402: module level import not at top of file (auto-generated noqa)  # noqa F401: 'collections' imported but unused (auto-generated noqa)
