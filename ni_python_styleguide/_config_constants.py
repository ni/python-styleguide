import pathlib

__FILE_DIR = pathlib.Path(__file__).parent

FLAKE8_CONFIG_FILE = __FILE_DIR / "config.ini"
BLACK_CONFIG_FILE = __FILE_DIR / "config.toml"
ISORT_CONFIG_FILE = BLACK_CONFIG_FILE
