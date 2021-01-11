import ni_python_styleguide._lint_errors_parser

import pytest

EXAMPLE_LINT_ERROR_LINES = [  # noqa W505
    r".\source\lorem.py:158:101: W505 doc line too long (186 > 100 characters)",
    r".\source\lorem.py:11:1: F401 'packaging.version.Version' imported but unused",
    r".\source\lorem.py:80:18: E711 comparison to None should be 'if cond is not None:'",
    r".\source\lorem.py:55:16: BLK100 Black would make changes.",
    r".\source\lorem.py:77:13: E741 ambiguous variable name 'l'",
    r".\source\lorem.py:111:13: F841 local variable 'data' is assigned to but never used",
    r".\source\lorem.py:8:11: E401 multiple imports on one line",
    r".\source\lorem.py:33:12: E713 test for membership should be 'not in'",
    r".\source\lorem.py:43:5: F811 redefinition of unused 'argparse' from line 7",
    r".\source\lorem.py:169:30: F821 undefined name 'option_values'",
    r".\source\lorem.py:33:9: F402 import 'entry' from line 8 shadowed by loop variable",
    r".\source\lorem.py:157:9: E722 do not use bare 'except'",
    r".\source\lorem.py:6:1: F403 'from ipsum import *' used; unable to detect undefined names",
    r".\source\lorem.py:123:23: F405 'sit' may be undefined, or defined from star imports: ipsum",
    r".\source\lorem.py:141:1: E402 module level import not at top of file",
    r".\source\lorem\ipsum.py:16:1: E731 do not assign a lambda expression, use a def",
    r".\tests\lorem\ipsum\dolor.py:49:9: E712 comparison to True should be 'if cond is True:' or 'if cond:'",
]


@pytest.mark.parametrize("input_line", EXAMPLE_LINT_ERROR_LINES)
def test_lint_errors_parser_handles_example_line_without_error(input_line):
    assert ni_python_styleguide._lint_errors_parser.parse(
        input_line
    ), "should parse without error and return object"
