"""Stack command group.

Commands that operate on your current stack of branches.
"""

import click


@click.group(name="stack")
def stack() -> None:
    """Commands that operate on your current stack of branches.

    Run `gt stack --help` to learn more.
    """
    pass
