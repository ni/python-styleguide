import ni_python_styleguide.lint_errors_parser

def _filter_to_handled_errors(lint_errors):
    not_handled_errors = {'BLK100'}
    return filter(lambda o: o not in not_handled_errors, lint_errors)

def _in_multiline_string(error_data: ni_python_styleguide.lint_errors_parser.LintError):
    with open(error_data.file) as in_file:
        lines = in_file.readlines()[:error_data.line]
    count_of_multiline_starts_and_stops = sum(line.count('"""') + line.count("'''") for line in lines)
    # if occurances of multiline string markers is odd, this must be in a multiline
    return count_of_multiline_starts_and_stops % 2 == 1


def acknowledge_lint_errors(lint_errors_file):
    lint_errors = []
    with open(lint_errors_file) as errors_input:
        for line in errors_input:
            lint_error = ni_python_styleguide.lint_errors_parser.parse(line)
            lint_errors.append(lint_error)
    lint_errors_to_process = _filter_to_handled_errors(lint_errors)
    for error in lint_errors_to_process:
        if _in_multiline_string(error):
            continue # TODO: handle this case by adding the marker at the end of the multiline
        with open(error.file, mode='r') as cache_file:
            code = cache_file.readlines()

        line = code[error.line - 1]
        line = line.rstrip('\n')
        line += f'  # NOQA {error.code}: {error.explanation} - This suppression was \n'
        'auto-generated to allow focus on handling new errors'
        code[error.line - 1] = line

        with open(error.file, mode='w') as out_file:
            for line in code:
                out_file.write(line)
