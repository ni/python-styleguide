from collections import defaultdict
import logging

import ni_python_styleguide._lint_errors_parser


def _filter_to_handled_errors(lint_errors):
    not_handled_errors = {"BLK100"}
    return filter(lambda o: o.code not in not_handled_errors, lint_errors)


def _in_multiline_string(error_file, lineno):
    with open(error_file) as in_file:
        lines = in_file.readlines()[:lineno]
    count_of_multiline_starts_and_stops = sum(
        line.count('"""') + line.count("'''") for line in lines
    )
    # if occurances of multiline string markers is odd, this must be in a multiline
    return count_of_multiline_starts_and_stops % 2 == 1


def _add_noqa_to_line(lineno, filepath, error_code, explanation):
    with open(filepath, mode="r") as cache_file:
        code = cache_file.readlines()

    line = code[lineno]
    line = line.rstrip("\n")
    line += (
        f"  # noqa {error_code}: {explanation} - This suppression was "
        "auto-generated to allow focus on handling new errors\n"
    )
    code[lineno] = line

    with open(filepath, mode="w") as out_file:
        for line in code:
            out_file.write(line)


def acknowledge_lint_errors(lint_errors):
    """Add a "noqa" comment for each of existing errors (unless excluded).

    Excluded error (reason):
    BLK100 - run black
    """
    parsed_errors = [ni_python_styleguide._lint_errors_parser.parse(error) for error in lint_errors]

    lint_errors_to_process = _filter_to_handled_errors(parsed_errors)
    # to avoid double marking a line with the same code, keep track of lines and codes
    handled_lines = defaultdict(list)
    for error in lint_errors_to_process:
        skip = 0
        if _in_multiline_string(error_file=error.file, lineno=error.line):
            # find when the multiline ends
            skip = 1
            while _in_multiline_string(error_file=error.file, lineno=error.line + skip):
                skip += 1

        cached_key = f"{error.file}:{error.line + skip}"
        if error.code in handled_lines.get(cached_key, []):
            logging.warning(
                "Multiple %s codes were logged for %s:%s, only suprressing first",
                error.code,
                error.file,
                error.line + skip,
            )
            continue

        handled_lines[cached_key].append(error.code)

        _add_noqa_to_line(
            lineno=error.line - 1 + skip,
            filepath=error.file,
            error_code=error.code,
            explanation=error.explanation,
        )
