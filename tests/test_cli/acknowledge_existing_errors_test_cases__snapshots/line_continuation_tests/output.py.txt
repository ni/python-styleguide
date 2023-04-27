some_string_with_line_continuation = f"{installPath}\\foo\\bar\\baz.exe \
      --check --this-is-cool --bacon --ipsum"  # noqa: D100, F821 - Missing docstring in public module (auto-generated noqa), undefined name 'installPath' (auto-generated noqa)

# black, please leave these ridiculous line continuations in place for testing.
# fmt: off
if 1 < 2 == True and \
    3 < 4 and \
        5 < 6:  # noqa: E712 - comparison to True should be 'if cond is True:' or 'if cond:' (auto-generated noqa)
    print("There is order in this world")
else:
    raise Exception("There's funny going on here.")
# fmt: on


someStringWithProblems = """
problems, I have # even if
putting the other quote in would be weird
but like I said: '''I got problems :|
# even some like this '''
many they be,
suppresion should be after
"""  # noqa: N816 - variable 'someStringWithProblems' in global scope should not be mixedCase (auto-generated noqa)

loremIpsum = "dolor"  # comments however are not affected \  # noqa: N816 - variable 'loremIpsum' in global scope should not be mixedCase (auto-generated noqa)
# even if they have backslashes
