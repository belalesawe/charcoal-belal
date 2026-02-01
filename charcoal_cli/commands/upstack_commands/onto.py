"""Upstack onto command.

Rebase the current branch onto a new base and restack all descendants.
"""

import click

from charcoal_cli.actions.current_branch_onto import current_branch_onto
from charcoal_cli.lib.context import create_context


@click.command(name="onto")
@click.argument("branch", required=False)
@click.option(
    "-s",
    "--source",
    help="Optional branch to rebase (defaults to current branch).",
    type=str,
)
@click.pass_context
def onto(ctx: click.Context, branch: str | None, source: str | None) -> None:
    """Rebase the current branch onto the latest commit of the target branch.

    Restacks all of its descendants. If no branch is passed in, opens an
    interactive selector.

    Args:
        branch: Optional branch to rebase the current stack onto
        source: Optional branch to rebase (defaults to current branch)
    """
    # Create context
    context = create_context()

    # Handle source branch if specified
    original_branch = None
    if source:
        original_branch = context.engine.current_branch
        context.engine.checkout_branch(source)

    # Get destination branch
    if not branch:
        # TODO: Implement interactive branch selection
        # For now, raise an error
        click.echo("Error: Branch argument is required (interactive selection not yet implemented)")
        ctx.exit(1)
        return

    # Perform the onto operation
    current_branch_onto(branch, context)

    # Restore original branch if needed
    if original_branch:
        context.engine.checkout_branch(original_branch)
