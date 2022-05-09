import pathlib
import tempfile
from contextlib import contextmanager


@contextmanager
def multi_access_tempfile(suffix=".txt", delete=True):
    """Tempfile that has been created and closed and will be deleted after this context.

    Used to allow writing to a temp file multiple times.
    """
    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp.close()
    temp_path = pathlib.Path(temp.name)
    try:
        yield temp_path
    finally:
        if delete:
            temp_path.unlink()
