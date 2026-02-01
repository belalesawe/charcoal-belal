"""Log default command.

Log all branches tracked by Charcoal, showing dependencies and info for each.
"""

import click

from charcoal_cli.actions.log import log_action
from charcoal_cli.lib.context import create_context


@click.command(name="default")
@click.option(
    "-r",
    "--reverse",
    is_flag=True,
    default=False,
    help="Print the log upside down. Handy when you have a lot of branches!",
)
@click.option(
    "-s",
    "--stack",
    is_flag=True,
    default=False,
    help="Only show ancestors and descendants of the current branch.",
)
@click.option(
    "-n",
    "--steps",
    type=int,
    default=None,
    help="Only show this many levels upstack and downstack. Implies --stack.",
)
@click.option(
    "-u",
    "--show-untracked",
    is_flag=True,
    default=False,
    help="Include untracked branches in interactive selection.",
)
@click.pass_context
def default(
    ctx: click.Context,
    reverse: bool,
    stack: bool,
    steps: int | None,
    show_untracked: bool,
) -> None:
    """Log all branches tracked by Charcoal, showing dependencies and info.

    This is the default log view with full information for each branch.

    Args:
        reverse: Print the log upside down
        stack: Only show ancestors and descendants of current branch
        steps: Number of levels to show upstack and downstack
        show_untracked: Include untracked branches
    """
    context = create_context()

    # Determine starting branch based on options
    if steps or stack:
        branch_name = context.engine.current_branch_precondition
    else:
        branch_name = context.engine.trunk

    log_action(
        {
            "style": "FULL",
            "reverse": reverse,
            "branchName": branch_name,
            "steps": steps,
            "showUntracked": show_untracked,
        },
        context,
    )
