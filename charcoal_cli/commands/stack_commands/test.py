"""Stack test command.

Run a command on each branch in the entire stack and aggregate results.
"""

import click

from charcoal_cli.actions.test import test_stack
from charcoal_cli.lib.context import create_context
from charcoal_cli.lib.engine.scope_spec import SCOPE


@click.command(name="test")
@click.argument("command")
@click.option(
    "-t",
    "--trunk",
    is_flag=True,
    default=False,
    help="Run the command on the trunk branch in addition to the rest of the stack.",
)
@click.pass_context
def test(ctx: click.Context, command: str, trunk: bool) -> None:
    """Run a command on each branch in the entire stack.

    Run the provided command on each branch in the current stack and
    aggregate the results.

    Args:
        command: The shell command to run on each branch
        trunk: Run the command on the trunk branch in addition to the rest
    """
    context = create_context()

    test_stack(
        {
            "scope": SCOPE.STACK,
            "includeTrunk": trunk,
            "command": command,
        },
        context,
    )
