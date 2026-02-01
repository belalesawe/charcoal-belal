"""Demo command to create a sample repository for tutorials."""

import click
import subprocess
import sys
import tempfile
from charcoal_cli.lib.utils.git_repo import GitRepo
from charcoal_cli.lib.utils.make_id import make_id


def _check_command_exists(command: list[str]) -> bool:
    """Check if a charcoal CLI command exists.

    Args:
        command: The command arguments to check (e.g., ['repo', 'init'])

    Returns:
        True if the command exists, False otherwise
    """
    import charcoal_cli
    from pathlib import Path

    cli_module_path = Path(charcoal_cli.__file__).parent / '__main__.py'

    result = subprocess.run(
        [sys.executable, str(cli_module_path)] + command + ['--help'],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


@click.command()
def demo() -> None:
    """Create a demo repository with sample branches for learning Charcoal.

    This command creates a temporary git repository with a sample branch stack
    that demonstrates Charcoal's workflow. The repository includes:
    - A review queue feature stack with multiple branches
    - Independent bug fix branches

    The repository path is printed to stdout so you can navigate to it and
    explore the branch structure.

    Note: This command requires the 'repo init' and 'branch create' commands
    to be implemented.
    """
    # Check if required commands exist
    if not _check_command_exists(['repo', 'init']):
        click.echo(
            "Error: The 'repo init' command is not available.\n"
            "The demo command requires 'repo init' and 'branch create' commands.\n"
            "These commands may not be migrated yet.",
            err=True
        )
        raise SystemExit(1)

    if not _check_command_exists(['branch', 'create']):
        click.echo(
            "Error: The 'branch create' command is not available.\n"
            "The demo command requires 'repo init' and 'branch create' commands.\n"
            "These commands may not be migrated yet.",
            err=True
        )
        raise SystemExit(1)

    # Create temporary directory
    tmp_dir = tempfile.mkdtemp(prefix='charcoal-demo-')

    click.echo(tmp_dir)

    # Initialize repository
    repo = GitRepo(tmp_dir)
    id_prefix = make_id(8)

    # Create initial commits on main
    repo.create_change_and_commit('First commit')
    repo.create_change_and_commit('Second commit')

    # Initialize charcoal repository
    repo.run_cli_command(['repo', 'init', '--no-interactive'])

    # Create review queue feature stack
    repo.create_change('[Product] Add review queue filter api')
    repo.run_cli_command([
        'branch',
        'create',
        f'{id_prefix}-review_queue_api',
        '-m',
        '[Product] Add review queue filter api',
    ])

    repo.create_change('[Product] Add review queue filter server')
    repo.run_cli_command([
        'branch',
        'create',
        f'{id_prefix}-review_queue_server',
        '-m',
        '[Product] Add review queue filter server',
    ])

    repo.create_change('[Product] Add review queue filter frontend')
    repo.run_cli_command([
        'branch',
        'create',
        f'{id_prefix}-review_queue_frontend',
        '-m',
        '[Product] Add review queue filter frontend',
    ])

    # Return to main for independent branches
    repo.checkout_branch('main')

    # Create first bug fix branch
    repo.create_change('[Bug Fix] Fix crashes on reload')
    repo.run_cli_command([
        'branch',
        'create',
        f'{id_prefix}-fix_crash_on_reload',
        '-m',
        '[Bug Fix] Fix crashes on reload',
    ])

    # Return to main for second bug fix
    repo.checkout_branch('main')

    # Create second bug fix branch
    repo.create_change('[Bug Fix] Account for empty state')
    repo.run_cli_command([
        'branch',
        'create',
        f'{id_prefix}-account_for_empty_state',
        '-m',
        '[Bug Fix] Account for empty state',
    ])

    # Return to main
    repo.checkout_branch('main')

    # Add remote (for demonstration, using graphite demo repo)
    repo.run_git_command([
        'remote',
        'add',
        'origin',
        'git@github.com:withgraphite/graphite-demo-repo.git',
    ])

    # Try to push to remote (matches TypeScript version behavior)
    # May fail without authentication, which is acceptable for a demo
    try:
        repo.run_git_command(['push', 'origin', 'main', '-f'])
    except Exception:
        # Push failed (likely due to authentication), but that's okay
        # The demo repo is still usable locally
        pass
