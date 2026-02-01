"""Downstack get command.

Get branches from trunk to the specified branch from remote.
"""

import click

from charcoal_cli.actions.sync.get import get_action
from charcoal_cli.lib.context import create_context


@click.command(name="get")
@click.argument("branch", required=False)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Overwrite all fetched branches with remote source of truth",
)
@click.pass_context
def get(ctx: click.Context, branch: str | None, force: bool) -> None:
    """Get branches from trunk to the specified branch from remote.

    Prompts the user to resolve conflicts. If no branch is provided, get
    downstack from the current branch.

    Args:
        branch: Branch to get from remote
        force: Overwrite all fetched branches with remote source of truth
    """
    context = create_context()

    get_action(
        {
            "branchName": branch,
            "force": force,
        },
        context,
    )
