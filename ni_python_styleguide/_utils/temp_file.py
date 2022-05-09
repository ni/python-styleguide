import pathlib
import tempfile
from contextlib import contextmanager


@contextmanager
def multi_access_tempfile(suffix=".txt", delete=True):
    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp.close()
    temp_path = pathlib.Path(temp.name)
    try:
        yield temp_path
    finally:
        if delete:
            temp_path.unlink()
