"""example of a python file with linter errors.
"""

import os

os.listdir()


def method_with_shadow_builtin(input):
    """Shadow a builtin."""
    return input


def method_with_shadow_import(os):
    """Shadow an import."""
    return os


def method_with_shadow_import_on_multiple_lines(
    x,
    y,
    os,
):
    """Shadow an import."""
    return os


def method_with_unused_param(unused_input):
    """Provide and unused param."""
    return 5


def method_with_parameters_on_multiple_lines(x, y):
    """Provide parameters on multiple lines test case."""
    return x + y


def method_with_bad_names_on_single_line(myBadlyNamedParam, my_other_Bad_name):
    """Provide parameters with bad names on single line."""
    return myBadlyNamedParam + my_other_Bad_name


def method_with_bad_names_on_multiple_lines_1(
    myBadlyNamedParam,
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + 5


def method_with_bad_names_on_multiple_lines_2(
    myBadlyNamedParam,
    my_other_Bad_name,
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + my_other_Bad_name


def method_withBadName_with_shadow(input):
    """Shadow a builtin."""
    return input


def method_withBadName_with_unused_param(unused_input):
    """Provide and unused param."""
    return 5


def method_withBadName_with_parameters_on_multiple_lines(x, y):
    """Provide parameters on multiple lines test case."""
    return x + y


def method_withBadName_with_bad_params_on_single_line(myBadlyNamedParam, my_other_Bad_name):
    """Provide parameters with bad names on single line."""
    return myBadlyNamedParam + my_other_Bad_name


def method_withBadName_with_bad_params_on_multiple_lines_1(
    myBadlyNamedParam,
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + 5


def method_withBadName_with_bad_params_on_multiple_lines_2(
    myBadlyNamedParam,
    my_other_Bad_name,
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + my_other_Bad_name
