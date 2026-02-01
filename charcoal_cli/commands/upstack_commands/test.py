"""Upstack test command.

Run a command on each branch in the upstack and aggregate results.
"""

import click

from charcoal_cli.actions.test import test_stack
from charcoal_cli.lib.context import create_context
from charcoal_cli.lib.engine.scope_spec import SCOPE


@click.command(name="test")
@click.argument("command")
@click.pass_context
def test(ctx: click.Context, command: str) -> None:
    """Run a command on each branch in the upstack.

    For each of the current branch and its descendants, run the provided
    command and aggregate the results.

    Args:
        command: The shell command to run on each branch
    """
    context = create_context()

    test_stack(
        {
            "scope": SCOPE.UPSTACK,
            "command": command,
        },
        context,
    )
