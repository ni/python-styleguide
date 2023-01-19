import pathlib
from typing import List, Optional

import ni_python_styleguide._utils


class InMultiLineStringChecker:
    """Provide utility methods to decide if line is within a multiline string."""

    def __init__(self, error_file: Optional[str] = None, *_, lines: Optional[List[str]] = None):
        """Cache off whether each line is in a multiline string or not."""
        self._values = []
        if error_file:
            self._error_file = pathlib.Path(error_file)
            self._load_lines()
        else:
            self._error_file = None
            if not lines:
                raise Exception(
                    "Error, must provide either path to `error_file` or provide `lines`"
                )
            self._set_lines(lines)

    @property
    def values(self):
        """The values for the file."""
        return self._values

    def in_multiline_string(self, lineno):
        """Checks if lineno is in a multiline string."""
        return self._values[lineno - 1]  # 0 indexed, but we number files 1 indexed

    @staticmethod
    def _count_multiline_string_endings_in_line(line):
        return line.count('"""'), line.count("'''")

    def _set_lines(self, lines):
        current_count = [0, 0]
        for line in lines:
            type1, type2 = InMultiLineStringChecker._count_multiline_string_endings_in_line(line)
            current_count[0] += type1
            current_count[1] += type2

            code_part_of_line = line
            if "#" in line:
                code_part_of_line = line.split("#", maxsplit=1)[0]

            # if occurrences of multiline string markers is odd, this must be in a multiline
            #  or, if line continuation token is on the ending, assume in a multiline statement
            self._values.append(
                any([part % 2 == 1 for part in current_count])
                or code_part_of_line.strip().endswith("\\")
            )

    def _load_lines(self):
        in_file = self._error_file.read_text(encoding=ni_python_styleguide._utils.DEFAULT_ENCODING)
        self._set_lines(in_file.splitlines())
