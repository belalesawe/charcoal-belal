"""Log long command.

Display a graph of the commit ancestry of all branches.
"""

import click

from charcoal_cli.lib.context import create_context


@click.command(name="long")
@click.pass_context
def long(ctx: click.Context) -> None:
    """Display a graph of the commit ancestry of all branches.

    This command shows the full git log with branch relationships.
    """
    context = create_context()

    # Call engine's log_long method
    context.engine.log_long()
