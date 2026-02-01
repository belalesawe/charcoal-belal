"""Action to track downstack branches.

This action sets up tracking for a series of untracked branches by specifying
each branch's parent.
"""

from charcoal_cli.lib.context import TContext


def track_stack(opts: dict, context: TContext) -> None:
    """Track a series of untracked branches.

    Args:
        opts: Options including 'branchName' and 'force'
        context: The application context
    """
    branch_name = opts.get("branchName")
    force = opts.get("force", False)

    # Stub implementation - actual tracking logic would go here
    context.splog.info(f"Tracking branches from {branch_name or 'current'}")
    if force:
        context.splog.info("Using force mode")
