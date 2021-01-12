"""example of a python file with linter errors.
"""

import os

os.listdir()


def _test_os_name():
    for os in range(3):
        print(os)
