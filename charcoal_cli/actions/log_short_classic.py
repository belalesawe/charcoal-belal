"""Classic short log format action.

This module provides the classic (old) logging style for short format logs.
"""

from charcoal_cli.lib.context import TContext


def display_branches_internal(
    opts: dict,
    context: TContext,
) -> list[dict]:
    """Display branches recursively in classic format.

    Args:
        opts: Options including:
            - branchName: Branch name to display
            - highlightCurrentBranch: Whether to highlight current branch
            - omitCurrentBranch: Whether to skip current branch
            - indent: Indentation level
        context: Application context

    Returns:
        List of dicts with 'display' and 'branchName' keys
    """
    current_branch_name = context.engine.current_branch
    indent_level = opts.get("indent", 0)
    branch_name = opts["branchName"]

    # Check if branch needs restack
    needs_restack = not context.engine.is_branch_fixed(branch_name)
    restack_msg = " \033[93m(needs restack)\033[0m" if needs_restack else ""

    current_choice = {
        "display": f"{'  ' * indent_level}↱ $ {branch_name}{restack_msg}",
        "branchName": branch_name,
    }

    # Get children
    children = context.engine.get_children(branch_name)
    if not children:
        return [current_choice]

    # Filter out current branch if requested
    omit_current = opts.get("omitCurrentBranch", False)
    if omit_current:
        children = [b for b in children if b != current_branch_name]

    # Recursively process children
    result = []
    for child in children:
        child_opts = {
            **opts,
            "branchName": child,
            "indent": indent_level + 1,
        }
        result.extend(display_branches_internal(child_opts, context))

    # Add current choice after children (classic bottom-up order)
    result.append(current_choice)

    return result


def log_short_classic(context: TContext) -> None:
    """Display log in classic short format.

    Args:
        context: Application context
    """
    branches = display_branches_internal(
        {"branchName": context.engine.trunk, "highlightCurrentBranch": True},
        context,
    )

    output = "\n".join(b["display"] for b in branches)
    context.splog.info(output)
