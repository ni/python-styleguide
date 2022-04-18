from ni_python_styleguide._acknowledge_existing_errors import _lint_errors_parser
from ni_python_styleguide import _lint

def get_lint_errors_to_process(exclude, app_import_names, extend_ignore, file_or_dir, excluded_errors):
    lint_errors = _lint.get_lint_output(
        format=None,
        qs_or_vs=None,
        exclude=exclude,
        app_import_names=app_import_names,
        extend_ignore=extend_ignore,
        file_or_dir=file_or_dir,
    ).splitlines()
    parsed_errors = map(_lint_errors_parser.parse, lint_errors)
    parsed_errors = list(filter(None, parsed_errors))
    lint_errors_to_process = [error for error in parsed_errors if error.code not in excluded_errors]
    return lint_errors_to_process
