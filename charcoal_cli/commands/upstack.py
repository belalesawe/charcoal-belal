"""Upstack command group.

Commands that operate on a branch and its descendants.
"""

import click


@click.group(name="upstack")
def upstack() -> None:
    """Commands that operate on a branch and its descendants.

    Run `gt upstack --help` to learn more.
    """
    pass
