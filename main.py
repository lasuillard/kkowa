#!/usr/bin/env -S poetry run python
from multiprocessing import freeze_support, set_start_method

from cli.root import cli

if __name__ == "__main__":
    freeze_support()
    set_start_method("spawn")
    cli()
