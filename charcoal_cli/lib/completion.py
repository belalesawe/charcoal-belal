"""Shell completion helpers for Charcoal CLI."""

import subprocess

import click


def complete_branch_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """Provide branch name completion for Click commands.

    Args:
        ctx: Click context (unused but required by Click API)
        param: Click parameter (unused but required by Click API)
        incomplete: Incomplete branch name being typed

    Returns:
        List of matching branch names
    """
    _ = ctx  # Unused but required by Click API
    _ = param  # Unused but required by Click API
    try:
        # Get all local branches
        result = subprocess.run(
            ['git', 'for-each-ref', '--format=%(refname:short)', 'refs/heads/'],
            capture_output=True,
            text=True,
            check=True,
        )
        branches = [b.strip() for b in result.stdout.strip().split('\n') if b.strip()]

        # Filter branches that match the incomplete string
        if incomplete:
            branches = [b for b in branches if b.startswith(incomplete)]

        return branches
    except subprocess.CalledProcessError:
        return []


def complete_remote_branch_name(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """Provide remote branch name completion for Click commands.

    Args:
        ctx: Click context (unused but required by Click API)
        param: Click parameter (unused but required by Click API)
        incomplete: Incomplete branch name being typed

    Returns:
        List of matching remote branch names
    """
    _ = ctx  # Unused but required by Click API
    _ = param  # Unused but required by Click API
    try:
        # Get all remote branches
        result = subprocess.run(
            ['git', 'for-each-ref', '--format=%(refname:strip=3)', 'refs/remotes/'],
            capture_output=True,
            text=True,
            check=True,
        )
        branches = [b.strip() for b in result.stdout.strip().split('\n') if b.strip()]

        # Filter branches that match the incomplete string
        if incomplete:
            branches = [b for b in branches if b.startswith(incomplete)]

        return branches
    except subprocess.CalledProcessError:
        return []
