"""Downstack track command.

Track a series of untracked branches by specifying each's parent.
"""

import click

from charcoal_cli.actions.track_branch import track_stack
from charcoal_cli.lib.context import create_context


@click.command(name="track")
@click.argument("branch", required=False)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Sets the parent of each branch to the most recent ancestor without interactive selection.",
)
@click.pass_context
def track(ctx: click.Context, branch: str | None, force: bool) -> None:
    """Track a series of untracked branches.

    By specifying each's parent. Starts at the current (or provided) branch
    and stops when you reach a tracked branch.

    Args:
        branch: Tip of the stack to begin tracking. Defaults to the current branch.
        force: Sets the parent of each branch to the most recent ancestor
    """
    context = create_context()

    track_stack(
        {
            "branchName": branch,
            "force": force,
        },
        context,
    )
