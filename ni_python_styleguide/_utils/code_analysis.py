import ast
import pathlib
from typing import Tuple


def find_import_region(file: pathlib.Path) -> Tuple[int, int]:
    """Return the index of the first last import line that precedes any other code.

    Note: will not handle try/except imports

    file: pathlib.Path path to file to evaluate
    Return: Tuple[int, int] the start and ending lines (0 based) of the module level imports
    """
    file_contents = file.read_text()
    tree = ast.parse(file_contents)
    end = start = 0
    for node in tree.body:  # only walk top level items
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            continue
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            continue
        end = node.lineno - 1
        break
    return start, end
