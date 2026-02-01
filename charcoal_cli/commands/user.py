"""User configuration command group.

This module provides the main 'user' command group for managing Charcoal CLI
user configuration settings.
"""

import click


@click.group(name="user")
def user() -> None:
    """Read or write Charcoal's user configuration settings.

    Run `charcoal user --help` to learn more.
    """
    pass
