some_string_with_line_continuation = f"{installPath}\\foo\\bar\\baz.exe \
      --check --this-is-cool --bacon --ipsum"

# black, please leave these ridiculous line continuations in place for testing.
# fmt: off
if 1 < 2 == True and \
    3 < 4 and \
        5 < 6:
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
"""

loremIpsum = "dolor"  # comments however are not affected \
# even if they have backslashes
