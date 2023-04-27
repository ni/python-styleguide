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


def method_with_bad_names_on_single_line(myBadlyNamedParam, my_other_Bad_name):  # noqa: N803 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa)
    """Provide parameters with bad names on single line."""
    return myBadlyNamedParam + my_other_Bad_name


def method_with_bad_names_on_multiple_lines_1(
    myBadlyNamedParam,  # noqa: N803 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa)
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + 5


def method_with_bad_names_on_multiple_lines_2(
    myBadlyNamedParam,  # noqa: N803 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa)
    my_other_Bad_name,
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + my_other_Bad_name


def method_withBadName_with_shadow(input):  # noqa: N802 - function name 'method_withBadName_with_shadow' should be lowercase (auto-generated noqa)
    """Shadow a builtin."""
    return input


def method_withBadName_with_unused_param(unused_input):  # noqa: N802 - function name 'method_withBadName_with_unused_param' should be lowercase (auto-generated noqa)
    """Provide and unused param."""
    return 5


def method_withBadName_with_parameters_on_multiple_lines(x, y):  # noqa: N802 - function name 'method_withBadName_with_parameters_on_multiple_lines' should be lowercase (auto-generated noqa)
    """Provide parameters on multiple lines test case."""
    return x + y


def method_withBadName_with_bad_params_on_single_line(myBadlyNamedParam, my_other_Bad_name):  # noqa:  N803, N802 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa), function name 'method_withBadName_with_bad_params_on_single_line' should be lowercase (auto-generated noqa)
    """Provide parameters with bad names on single line."""
    return myBadlyNamedParam + my_other_Bad_name


def method_withBadName_with_bad_params_on_multiple_lines_1(  # noqa: N802 - function name 'method_withBadName_with_bad_params_on_multiple_lines_1' should be lowercase (auto-generated noqa)
    myBadlyNamedParam,  # noqa: N803 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa)
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + 5


def method_withBadName_with_bad_params_on_multiple_lines_2(  # noqa: N802 - function name 'method_withBadName_with_bad_params_on_multiple_lines_2' should be lowercase (auto-generated noqa)
    myBadlyNamedParam,  # noqa: N803 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa)
    my_other_Bad_name,
):
    """Provide parameters with bad names on multiple lines."""
    return myBadlyNamedParam + my_other_Bad_name


def method_withBadName_andParams(my_normal_param, myBadlyNamedParam, my_other_Bad_param):  # noqa:  N803, N802 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa), function name 'method_withBadName_andParams' should be lowercase (auto-generated noqa)
    """Provide example where black will want to split out result."""
    return 5 + 7


def method_withBadName_and_bad_param_with_long_name(  # noqa: N802 - function name 'method_withBadName_and_bad_param_with_long_name' should be lowercase (auto-generated noqa)
    my_normal_param, myBadlyNamedParam, my_other_Bad_param  # noqa: N803 - argument name 'myBadlyNamedParam' should be lowercase (auto-generated noqa)
):
    """Provide example where black will want to split out result even more"""  # noqa:  D415, W505 - First line should end with a period, question mark, or exclamation point (auto-generated noqa), doc line too long (188 > 100 characters) (auto-generated noqa)
    return 5 + 7
