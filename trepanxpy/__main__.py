"""A main program for trepan-xpy."""
import sys
import click
from typing import List

from trepanxpy.version import VERSION
from trepanxpy.debugger import Debugger

@click.command()
@click.version_option(VERSION, "-V", "--version")
@click.argument("path", nargs=1, type=click.Path(readable=True), required=False)
@click.argument("args", nargs=-1)
def main(path: str, args: List[str]):

    # FIXME: This seems to be needed for pyficache to work on relative paths.
    # is this a bug?
    sys.path.append(".")

    Debugger(path, args)

if __name__ == "__main__":
    main(auto_envvar_prefix="XPYTHON")