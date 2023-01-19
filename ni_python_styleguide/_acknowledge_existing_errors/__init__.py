import logging
import pathlib
import re
from collections import defaultdict

from ni_python_styleguide import _format
from ni_python_styleguide import _utils

_module_logger = logging.getLogger(__name__)

EXCLUDED_ERRORS = {
    "BLK100",
}


def _add_noqa_to_line(lineno, code_lines, error_code, explanation):
    line = code_lines[lineno]
    old_line_ending = "\n" if line.endswith("\n") else ""
    line = line.rstrip("\n")

    if f"noqa {error_code}" not in line:
        prefix = "  " if line.strip() else ""
        line += f"{prefix}# noqa {error_code}: {explanation} (auto-generated noqa)"

    code_lines[lineno] = line + old_line_ending


def _filter_suppresion_from_line(line: str):
    if "(auto-generated noqa)" in line:
        return re.sub(r"# noqa .+\(auto-generated noqa\)", "", line).rstrip()
    else:
        return line


def acknowledge_lint_errors(
    exclude, app_import_names, extend_ignore, file_or_dir, *_, aggressive=False
):
    """Adds a "noqa" comment for each of existing errors (unless excluded).

    Excluded error (reason):
    BLK100 - run black
    """
    lint_errors_to_process = _utils.lint.get_errors_to_process(
        exclude,
        app_import_names,
        extend_ignore,
        [pathlib.Path(file_or_dir_) for file_or_dir_ in file_or_dir or "."],
        excluded_errors=EXCLUDED_ERRORS,
    )

    lint_errors_by_file = defaultdict(list)
    for error in lint_errors_to_process:
        lint_errors_by_file[pathlib.Path(error.file)].append(error)

    failed_files = []
    for bad_file, errors_in_file in lint_errors_by_file.items():
        _suppress_errors_in_file(bad_file, errors_in_file, encoding=_utils.DEFAULT_ENCODING)

        if aggressive:
            # some cases are expected to take up to 4 passes, making this 2x rounded
            per_file_format_iteration_limit = 10
            for _ in range(per_file_format_iteration_limit):
                # format the files - this may move the suppression off the correct lines
                #  Note: due to Github pycodestyle#868, we have to format, change, format
                #   (check if that time made changes)
                # -  else we wind up with lambda's going un-suppressed
                # and/or not re-formatted (to fail later)
                _format.format(bad_file)

                # re-apply suppressions on correct lines
                remove_auto_suppressions_from_file(bad_file)
                current_lint_errors = _utils.lint.get_errors_to_process(
                    exclude=exclude,
                    app_import_names=app_import_names,
                    extend_ignore=extend_ignore,
                    file_or_dir=file_or_dir,
                    excluded_errors=EXCLUDED_ERRORS,
                )

                _suppress_errors_in_file(
                    bad_file, current_lint_errors, encoding=_utils.DEFAULT_ENCODING
                )

                changed = _format.format_check(bad_file)
                if not changed:  # are we done?
                    break
            else:
                failed_files.append(
                    f"Could not handle suppressions/formatting of file {bad_file} after maximum number of tries ({per_file_format_iteration_limit})"
                )
                _module_logger.warning("Max tries reached on %s", bad_file)
    if failed_files:
        raise RuntimeError("Could not handle some files:\n" + "\n\n".join(failed_files) + "\n\n\n")


def remove_auto_suppressions_from_file(file: pathlib.Path):
    """Removes auto-suppressions from file."""
    lines = file.read_text(encoding=_utils.DEFAULT_ENCODING).splitlines()
    stripped_lines = [_filter_suppresion_from_line(line) for line in lines]
    file.write_text("\n".join(stripped_lines) + "\n", encoding=_utils.DEFAULT_ENCODING)


def _suppress_errors_in_file(bad_file, errors_in_file, encoding):
    path = pathlib.Path(bad_file)
    lines = path.read_text(encoding=encoding).splitlines(keepends=True)
    # sometimes errors are reported on line 1 for empty files.
    # to make suppressions work for those cases, add an empty line.
    if len(lines) == 0:
        lines = ["\n"]
    multiline_checker = _utils.string_helpers.InMultiLineStringChecker(error_file=bad_file)

    # to avoid double marking a line with the same code, keep track of lines and codes
    handled_lines = defaultdict(list)
    for error in errors_in_file:
        skip = 0

        while error.line + skip < len(lines) and multiline_checker.in_multiline_string(
            lineno=error.line + skip
        ):
            # find when the multiline ends
            skip += 1

        cached_key = f"{error.file}:{error.line + skip}"
        if error.code in handled_lines[cached_key]:
            _module_logger.warning(
                "Multiple occurrences of error %s code were logged for %s:%s, only supressing first",
                error.code,
                error.file,
                error.line + skip,
            )
            continue

        handled_lines[cached_key].append(error.code)

        _add_noqa_to_line(
            lineno=error.line - 1 + skip,
            code_lines=lines,
            error_code=error.code,
            explanation=error.explanation,
        )

    path.write_text("".join(lines), encoding=encoding)
