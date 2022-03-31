import fnmatch
import os
import pathlib

from git import GitError, repo


def find_repo_root(cwd: os.PathLike):
    """Find the Git repo path or return None."""
    try:
        _repo = repo.Repo(str(cwd), search_parent_directories=True)
    except GitError:
        return None
    return _repo.working_tree_dir


def get_tracked_files(cwd: os.PathLike, *_, branch: str = "main", filter: str = "*.*"):
    """Get all Git tracked files under cwd."""
    cwd = pathlib.Path(cwd)
    _repo = repo.Repo(str(cwd), search_parent_directories=True)
    repo_root = pathlib.Path(_repo.working_dir)
    output = _repo.git.ls_tree(str(cwd), r=branch, name_only=True).splitlines()
    for line in output:
        if line.startswith(str(cwd)) and fnmatch.fnmatch(line, filter):
            yield repo_root / line
