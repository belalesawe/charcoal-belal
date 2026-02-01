"""Classic short log format action.

This action provides the old-style logging format that shows branch hierarchies
in a simple tree structure with indentation.
"""

from typing import TypedDict

from charcoal_cli.lib.colors import RESET
from charcoal_cli.lib.context import TContext


class BranchDisplay(TypedDict):
    """Type for branch display information."""

    display: str
    branchName: str


def display_branches_internal(
    opts: dict,
    context: TContext,
) -> list[BranchDisplay]:
    """Recursively build branch display list.

    Args:
        opts: Options including:
            - branchName: Name of the branch to display
            - highlightCurrentBranch: Whether to highlight current branch
            - omitCurrentBranch: Whether to skip current branch
            - indent: Indentation level for display
        context: Application context

    Returns:
        List of branch display dictionaries
    """
    branch_name = opts["branchName"]
    indent = opts.get("indent", 0)
    omit_current = opts.get("omitCurrentBranch", False)

    current_branch_name = context.engine.current_branch

    # Build display string for current branch
    needs_restack = not context.engine.is_branch_fixed(branch_name)
    restack_indicator = " (needs restack)" if needs_restack else ""

    # Use yellow color for needs restack indicator
    if needs_restack:
        restack_indicator = f"\033[93m{restack_indicator}{RESET}"

    current_choice: BranchDisplay = {
        "display": f"{'  ' * indent}↱ $ {branch_name}{restack_indicator}",
        "branchName": branch_name,
    }

    # Get children and recursively display them
    children = context.engine.get_children(branch_name)

    if not children:
        return [current_choice]

    # Filter out current branch if needed
    filtered_children = [
        child for child in children
        if child != current_branch_name or not omit_current
    ]

    # Recursively build displays for children
    child_displays = []
    for child in filtered_children:
        child_opts = {
            **opts,
            "branchName": child,
            "indent": indent + 1,
        }
        child_displays.append(display_branches_internal(child_opts, context))

    # Combine current with children (children before current in reverse order)
    result = [current_choice]
    for child_list in reversed(child_displays):
        result = child_list + result

    return result


def log_short_classic(context: TContext) -> None:
    """Display branches in classic short log format.

    Args:
        context: Application context
    """
    branches = display_branches_internal(
        {
            "branchName": context.engine.trunk,
            "highlightCurrentBranch": True,
        },
        context,
    )

    output = "\n".join(branch["display"] for branch in branches)
    context.splog.info(output)
