"""example of a python file with linter errors.
"""

import os

os.listdir()


def _test_os_name():
    for os in range(3):  # NOQA F402: import 'os' from line 4 shadowed by loop variable - This suppression was auto-generated to allow focus on handling new errors
        print(os)
