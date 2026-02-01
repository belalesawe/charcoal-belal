"""Log short command.

Log all stacks tracked by Charcoal, arranged to show dependencies.
"""

import click

from charcoal_cli.actions.log import log_action
from charcoal_cli.actions.log_short_classic import log_short_classic
from charcoal_cli.lib.context import create_context


@click.command(name="short")
@click.option(
    "-c",
    "--classic",
    is_flag=True,
    default=False,
    help="Use the old logging style, which runs out of screen real estate quicker. Other options will not work in classic mode.",
)
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
def short(
    ctx: click.Context,
    classic: bool,
    reverse: bool,
    stack: bool,
    steps: int | None,
    show_untracked: bool,
) -> None:
    """Log all stacks tracked by Charcoal, arranged to show dependencies.

    This is the compact short view that uses box-drawing characters for visualization.
    """
    context = create_context()

    if classic:
        # Use classic logging style
        log_short_classic(context)
    else:
        # Determine which branch to start from
        if steps or stack:
            branch_name = context.engine.current_branch_precondition
        else:
            branch_name = context.engine.trunk

        log_action(
            {
                "style": "SHORT",
                "reverse": reverse,
                "branchName": branch_name,
                "steps": steps,
                "showUntracked": show_untracked,
            },
            context,
        )
