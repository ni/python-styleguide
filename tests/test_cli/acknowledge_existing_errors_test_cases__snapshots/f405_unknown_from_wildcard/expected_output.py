"""example of a python file with linter errors.
"""

from os.path import *  # NOQA F403: 'from os.path import *' used; unable to detect undefined names - This suppression was auto-generated to allow focus on handling new errors

listdir()  # NOQA F405: 'listdir' may be undefined, or defined from star imports: os.path - This suppression was auto-generated to allow focus on handling new errors
