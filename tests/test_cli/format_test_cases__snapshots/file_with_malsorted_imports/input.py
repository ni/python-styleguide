from datetime import datetime
from typing import List, Dict, Any
import ni_python_styleguide
import os
import logging
import click

@click.command()
def _main():
    now = datetime.now()
    v: List[Any] = [now]
    print(v)
    y: Dict[List, str] = {v: "value"}
    print(y)
    print(now)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Running ni-python-styleguide")
    ni_python_styleguide.main()
    logger.info("ni-python-styleguide dir %s", os.path.dirname(ni_python_styleguide.__file__))
