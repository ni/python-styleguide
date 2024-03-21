import ni_python_styleguide
import os
import logging


def _main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Running ni-python-styleguide")
    ni_python_styleguide.main()
    logger.info("ni-python-styleguide dir %s", os.path.dirname(ni_python_styleguide.__file__))
