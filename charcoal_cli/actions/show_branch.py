"""Branch information display action.

This action provides functions for displaying detailed branch information
including commit counts, PR status, and other metadata.
"""

from charcoal_cli.lib.context import TContext


def get_branch_info(branch_name: str, context: TContext) -> str:
    """Get formatted branch information for display.

    Args:
        branch_name: Name of the branch to get info for
        context: Application context

    Returns:
        Formatted string with branch information
    """
    # Stub implementation - in the full version this would return:
    # - Commit count
    # - PR status
    # - Branch description
    # - Merge status
    # For now, return basic information
    is_trunk = context.engine.is_trunk(branch_name)
    if is_trunk:
        return "(trunk)"

    # Get parent for context
    parent = context.engine.get_parent(branch_name)
    if parent:
        return f"→ {parent}"

    return ""
