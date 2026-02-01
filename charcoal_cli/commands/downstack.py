"""Downstack command group.

Commands that operate on a branch and its ancestors.
"""

import click


@click.group(name="downstack")
def downstack() -> None:
    """Commands that operate on a branch and its ancestors.

    Run `gt downstack --help` to learn more.
    """
    pass
