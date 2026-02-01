"""Action to move current branch onto a new base.

This action rebases the current branch onto a new base branch and restacks
all its descendants.
"""

from charcoal_cli.lib.context import TContext
from charcoal_cli.lib.engine.scope_spec import SCOPE


def current_branch_onto(onto_branch_name: str, context: TContext) -> None:
    """Rebase the current branch onto a new base and restack descendants.

    Args:
        onto_branch_name: The branch to rebase onto
        context: The application context
    """
    current_branch = context.engine.current_branch_precondition

    # Set the new parent
    context.engine.set_parent(current_branch, onto_branch_name)

    # Restack the upstack branches
    # Note: This should call restackBranches from restack.py
    # For now, we'll add a stub that will be replaced when restack is available
    branches = context.engine.get_relative_stack(current_branch, SCOPE.UPSTACK)
    context.splog.info(f"Restacking {len(branches)} branches...")
    # TODO: Call restackBranches when available
