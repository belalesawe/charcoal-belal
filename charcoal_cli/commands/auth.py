"""Authentication command for GitHub CLI integration."""

import click
import subprocess
import re


MIN_GH_VERSION = '2.0.0'


def get_gh_version() -> str | None:
    """Get the installed GitHub CLI version.

    Returns:
        Version string or None if gh is not installed
    """
    try:
        result = subprocess.run(
            ['gh', '--version'],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return None

        match = re.search(r'gh version (\d+\.\d+\.\d+)', result.stdout)
        return match.group(1) if match else None
    except FileNotFoundError:
        return None


def get_github_authorization_status() -> bool:
    """Check if GitHub CLI is authenticated.

    Returns:
        True if authenticated, False otherwise
    """
    try:
        result = subprocess.run(
            ['gh', 'auth', 'status'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings.

    Args:
        version1: First version string (e.g., "2.0.0")
        version2: Second version string (e.g., "1.5.0")

    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    v1_parts = [int(x) for x in version1.split('.')]
    v2_parts = [int(x) for x in version2.split('.')]

    for i in range(max(len(v1_parts), len(v2_parts))):
        v1 = v1_parts[i] if i < len(v1_parts) else 0
        v2 = v2_parts[i] if i < len(v2_parts) else 0
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
    return 0


@click.command()
@click.option(
    '-t',
    '--token',
    type=str,
    help='Authenticate with the GitHub API using OAuth.',
)
def auth(token: str | None) -> None:
    """Authenticate with the GitHub CLI to create and manage PRs in GitHub from Charcoal."""
    # Note: token parameter is defined for compatibility but currently unused
    # Authentication is delegated to gh CLI which handles OAuth flow
    _ = token  # Mark as intentionally unused

    gh_version = get_gh_version()

    if not gh_version or compare_versions(gh_version, MIN_GH_VERSION) < 0:
        click.echo(f'Error: Please install GitHub CLI version {MIN_GH_VERSION} or higher.')
        return

    is_gh_authorized = get_github_authorization_status()

    if is_gh_authorized:
        click.echo('Already authenticated with GitHub.')
        return

    click.echo('Charcoal is not authenticated with GitHub. Please authenticate.')

    try:
        subprocess.run(
            ['gh', 'auth', 'login'],
            stdin=None,
            stdout=None,
            stderr=None,
        )
        click.echo('Successfully authenticated Charcoal with GitHub.')
    except (FileNotFoundError, subprocess.CalledProcessError):
        click.echo('Error: Failed to authenticate Charcoal with GitHub. Please try again.')
