"""Log visualization actions.

This module provides the core log visualization logic for displaying branch
stacks with tree structures, colors, and branch information.
"""

from typing import TypedDict

from charcoal_cli.lib.colors import RESET, get_log_short_color
from charcoal_cli.lib.context import TContext


class LogOptions(TypedDict, total=False):
    """Options for log display."""

    style: str  # 'SHORT' or 'FULL'
    reverse: bool
    steps: int | None
    branchName: str
    showUntracked: bool


def get_untracked_branch_names(context: TContext) -> list[str]:
    """Get list of untracked branch names.

    Args:
        context: Application context

    Returns:
        List of untracked branch names
    """
    return [
        branch_name
        for branch_name in context.engine.all_branch_names
        if not context.engine.is_trunk(branch_name)
        and not context.engine.is_branch_tracked(branch_name)
    ]


def log_action(opts: LogOptions, context: TContext) -> None:
    """Display log visualization.

    Args:
        opts: Log display options including style, reverse, steps, etc.
        context: Application context
    """
    is_short = opts.get("style") == "SHORT"
    reverse = opts.get("reverse", False)
    branch_name = opts["branchName"]
    steps = opts.get("steps")
    show_untracked = opts.get("showUntracked", False)

    # Get stack lines
    log_lines = get_stack_lines(
        {
            "short": is_short,
            "reverse": reverse,
            "branchName": branch_name,
            "indentLevel": 0,
            "steps": steps,
        },
        context,
    )

    # Add untracked branches if requested
    if show_untracked:
        untracked = get_untracked_branch_names(context)
        if untracked:
            log_lines.append("")
            log_lines.append("\033[93mUntracked branches:\033[0m")
            log_lines.extend(untracked)

    # Join and page output
    log_output = "\n".join(log_lines)
    context.splog.page(log_output)


def log_for_conflict_status(rebase_head: str, context: TContext) -> None:
    """Display log for conflict status.

    Shows a limited stack view during rebase conflicts.

    Args:
        rebase_head: Branch name being rebased
        context: Application context
    """
    lines = get_stack_lines(
        {
            "short": True,
            "reverse": False,
            "branchName": rebase_head,
            "indentLevel": 0,
            "steps": 1,
            "noStyleBranchName": True,
        },
        context,
    )

    for line in lines:
        context.splog.info(line)


def interactive_branch_selection(
    opts: dict,
    context: TContext,
) -> str:
    """Interactive branch selection with autocomplete.

    Note: This function is synchronous. In the full implementation,
    it would integrate with an async prompt system, but for now it
    uses the synchronous stub.

    Args:
        opts: Options including:
            - message: Prompt message
            - omitCurrentBranch: Whether to skip current branch
            - showUntracked: Whether to include untracked branches
        context: Application context

    Returns:
        Selected branch name
    """
    import re

    message = opts["message"]
    omit_current = opts.get("omitCurrentBranch", False)
    show_untracked = opts.get("showUntracked", False)

    # Get stack lines for choices
    stack_lines = get_stack_lines(
        {
            "short": True,
            "reverse": False,
            "branchName": context.engine.trunk,
            "indentLevel": 0,
            "omitCurrentBranch": omit_current,
            "noStyleBranchName": True,
        },
        context,
    )

    # Build choices - extract branch name from each line
    choices = []
    for line in stack_lines:
        # Strip ANSI codes and extract branch name (last part after spaces)
        clean_line = re.sub(r'\033\[[0-9;]+m', '', line)
        # Branch name is after the last "  " sequence
        branch_name = clean_line[clean_line.rfind("  ") + 2:].strip()
        if branch_name:  # Only add non-empty branch names
            choices.append({"title": line, "value": branch_name})

    # Add untracked branches
    if show_untracked:
        for branch_name in get_untracked_branch_names(context):
            choices.append({"title": branch_name, "value": branch_name})

    # Find index of current branch (or parent if omit current)
    target_branch = context.engine.current_branch
    if omit_current and target_branch:
        parent = context.engine.get_parent_precondition(target_branch)
        target_branch = parent

    initial = len(choices) - 1
    for i, choice in enumerate(choices):
        if choice["value"] == target_branch:
            initial = i
            break

    # Use prompts system (synchronous in stub implementation)
    # In real implementation this would be async but we keep it sync for now
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(context.prompts({
            "type": "autocomplete",
            "name": "branch",
            "message": message,
            "choices": choices,
            "initial": initial,
        }))
    except RuntimeError:
        # No event loop, call directly (works with stub)
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(context.prompts({
            "type": "autocomplete",
            "name": "branch",
            "message": message,
            "choices": choices,
            "initial": initial,
        }))
        loop.close()

    chosen_branch = result["branch"]
    context.splog.debug(f"Selected {chosen_branch}")
    return chosen_branch


def get_stack_lines(args: dict, context: TContext) -> list[str]:
    """Get formatted stack lines for display.

    Args:
        args: Arguments including:
            - short: Whether to use short format
            - reverse: Whether to reverse output
            - branchName: Starting branch name
            - indentLevel: Indentation level
            - steps: Number of levels to show
            - omitCurrentBranch: Whether to skip current branch
            - noStyleBranchName: Whether to skip styling branch names
        context: Application context

    Returns:
        List of formatted lines
    """
    is_short = args.get("short", False)
    reverse_order = args.get("reverse", False)
    branch_name = args["branchName"]
    steps = args.get("steps")

    overall_indent = {"value": 0}

    # Get upstack, current, and downstack lines
    upstack_lines = get_upstack_exclusive_lines(
        {**args, "overallIndent": overall_indent}, context
    )
    current_lines = get_branch_lines(args, context)
    downstack_lines = get_downstack_exclusive_lines(args, context)

    # Combine in order
    if reverse_order:
        all_lines = downstack_lines + current_lines + upstack_lines
    else:
        all_lines = upstack_lines + current_lines + downstack_lines

    # Apply short format styling if needed
    if is_short:
        all_lines = apply_short_format_styling(
            all_lines, overall_indent, args, context
        )

    return all_lines


def apply_short_format_styling(
    lines: list[str],
    overall_indent: dict,
    args: dict,
    context: TContext,
) -> list[str]:
    """Apply color styling to short format lines.

    Args:
        lines: Lines to style
        overall_indent: Overall indent tracking
        args: Display arguments
        context: Application context

    Returns:
        Styled lines
    """
    styled_lines = []
    no_style = args.get("noStyleBranchName", False)
    current_branch = context.engine.current_branch

    for line in lines:
        # Find circle and arrow positions
        circle_idx = line.find('◯')
        arrow_idx = line.find('▸')

        if arrow_idx == -1:
            styled_lines.append(line)
            continue

        # Extract branch name and details
        branch_and_details = line[arrow_idx + 1:].strip()
        branch_name_part = branch_and_details.split(' ')[0] if branch_and_details else ""

        # Check if this is the current branch
        is_current = (
            not no_style
            and current_branch
            and branch_name_part == current_branch
        )

        # Color the tree structure characters
        tree_part = line[:arrow_idx]
        colored_tree = ""
        for i, char in enumerate(tree_part):
            color = get_log_short_color(circle_idx if circle_idx != -1 else i)
            # Replace empty circle with filled circle for current branch
            if is_current and char == '◯':
                colored_tree += color + '◉' + RESET
            else:
                colored_tree += color + char + RESET

        # Color the branch name part
        color = get_log_short_color(circle_idx if circle_idx != -1 else 0)
        colored_branch = color + branch_and_details + RESET

        # Add spacing
        spacing = ' ' * (overall_indent["value"] * 2 + 3 - arrow_idx)

        styled_line = colored_tree + spacing + colored_branch
        styled_lines.append(styled_line)

    return styled_lines


def get_upstack_exclusive_lines(args: dict, context: TContext) -> list[str]:
    """Get lines for upstack branches (exclusive of current).

    Args:
        args: Display arguments
        context: Application context

    Returns:
        List of formatted lines for upstack
    """
    branch_name = args["branchName"]
    steps = args.get("steps")
    is_short = args.get("short", False)
    omit_current = args.get("omitCurrentBranch", False)

    children = context.engine.get_children(branch_name)
    if not children:
        return []

    # Filter children if needed
    if omit_current:
        current = context.engine.current_branch
        children = [c for c in children if c != current]

    # Recursively get lines for each child
    result_lines = []
    for child in children:
        child_args = {
            **args,
            "branchName": child,
            "indentLevel": args.get("indentLevel", 0) + 1,
        }
        result_lines.extend(get_stack_lines(child_args, context))

    return result_lines


def get_branch_lines(args: dict, context: TContext) -> list[str]:
    """Get lines for the current branch.

    Args:
        args: Display arguments
        context: Application context

    Returns:
        List of formatted lines for current branch
    """
    branch_name = args["branchName"]
    indent_level = args.get("indentLevel", 0)
    is_short = args.get("short", False)

    if is_short:
        # Short format uses Unicode box characters
        indent = '◯' * indent_level
        line = f"{indent}▸ {branch_name}"
    else:
        # Full format includes more details
        indent_str = "  " * indent_level
        # Get branch info if available
        try:
            from charcoal_cli.actions.show_branch import get_branch_info
            branch_info = get_branch_info(branch_name, context)
            if branch_info:
                line = f"{indent_str}◯ {branch_name} - {branch_info}"
            else:
                line = f"{indent_str}◯ {branch_name}"
        except (ImportError, AttributeError):
            # If show_branch module is not available, just show branch name
            line = f"{indent_str}◯ {branch_name}"

    return [line]


def get_downstack_exclusive_lines(args: dict, context: TContext) -> list[str]:
    """Get lines for downstack branches (exclusive of current).

    Args:
        args: Display arguments
        context: Application context

    Returns:
        List of formatted lines for downstack
    """
    branch_name = args["branchName"]
    steps = args.get("steps")

    # If we're already at trunk, no downstack
    if context.engine.is_trunk(branch_name):
        return []

    # Get parent chain from trunk to current
    parents = []
    current = branch_name
    while current and not context.engine.is_trunk(current):
        parent = context.engine.get_parent(current)
        if parent:
            parents.append(parent)
            current = parent
        else:
            break

    # Add trunk
    if not parents or parents[-1] != context.engine.trunk:
        parents.append(context.engine.trunk)

    # Reverse to go from trunk up
    parents.reverse()

    # Limit by steps if specified
    if steps is not None and steps > 0:
        parents = parents[-steps:]

    # Format each parent
    result_lines = []
    for i, parent_name in enumerate(parents):
        parent_args = {
            **args,
            "branchName": parent_name,
            "indentLevel": 0,  # Parents are at root level
        }
        result_lines.extend(get_branch_lines(parent_args, context))

    return result_lines
