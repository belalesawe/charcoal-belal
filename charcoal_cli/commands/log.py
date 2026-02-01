"""Log command group.

Commands that log your stacks and branch hierarchies.
"""

import click


@click.group(name="log")
def log() -> None:
    """Commands that log your stacks.

    Run `gt log --help` to learn more about visualization options.
    """
    pass


# Aliases for the command group will be registered in cli.py
