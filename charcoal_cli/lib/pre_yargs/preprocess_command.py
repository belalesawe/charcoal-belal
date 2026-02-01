"""Command preprocessing and shortcut expansion.

This module coordinates the pre-processing of command-line arguments before
Click processes them. It handles:
1. Git command passthrough
2. Shortcut expansion (e.g., 'bco' -> ['b', 'co'])
3. Deprecated command checking
"""

import sys
from typing import Optional

from charcoal_cli.lib.pre_yargs.deprecated_commands import (
    handle_deprecated_command_names,
)
from charcoal_cli.lib.pre_yargs.passthrough import passthrough


def split_shortcuts(command: str) -> list[str]:
    """Split shortcut commands into their constituent parts.

    This handles special shortcut patterns like:
    - Two-letter shortcuts (except 'ds', 'us' which are noun aliases)
    - Three-letter shortcuts like 'bco', 'bdl', etc.
    - Four-letter shortcuts like 'dstr'

    Args:
        command: The command string to potentially split

    Returns:
        List of command parts (may be just [command] if no splitting occurs)

    Examples:
        >>> split_shortcuts("bco")
        ['b', 'co']
        >>> split_shortcuts("ds")
        ['ds']
        >>> split_shortcuts("dsg")
        ['ds', 'g']
        >>> split_shortcuts("dstr")
        ['ds', 'tr']
    """
    # Two-letter commands (except 'ds', 'us' which are noun aliases)
    if len(command) == 2 and command not in ("ds", "us"):
        return [command[0], command[1]]

    # Three-letter shortcuts with specific patterns
    if len(command) == 3 and command in (
        "bco",
        "bdl",
        "btr",
        "but",
        "brn",
        "bsq",
        "bsp",
        "dpr",
    ):
        return [command[0], command[1:]]

    # Three-letter commands starting with two-letter noun aliases
    if len(command) == 3 and command[:2] in ("ds", "us"):
        return [command[:2], command[2]]

    # Four-letter shortcuts like 'dstr'
    if len(command) == 4 and command in ("dstr",):
        return [command[:2], command[2:]]

    # No shortcut expansion needed
    return [command]


def get_click_input(argv: Optional[list[str]] = None) -> list[str]:
    """Get and preprocess command-line input for Click.

    This function:
    1. Checks for git passthrough commands (exits if matched)
    2. Expands shortcuts (e.g., 'bco' -> ['b', 'co'])
    3. Checks for deprecated commands (may exit with error)
    4. Returns processed arguments for Click

    Args:
        argv: Command-line arguments (defaults to sys.argv if not provided)

    Returns:
        Processed list of command arguments for Click to parse
    """
    if argv is None:
        argv = sys.argv

    # Check for passthrough first (may exit)
    passthrough(argv)

    # If we have fewer than 2 args (program name + at least 1 command),
    # return empty list (will show help)
    if len(argv) < 2:
        return []

    # Expand shortcuts and build the command list
    # argv[0] is the program name (e.g., '__main__.py' or 'gt')
    # argv[1] is the first actual command
    # For Python: sys.argv = ['__main__.py', 'branch', 'next']
    # For installed binary: sys.argv = ['gt', 'branch', 'next']
    # First command token may need expansion (e.g., 'bco' → ['b', 'co'])
    expanded_command = split_shortcuts(argv[1])
    click_input = expanded_command + list(argv[2:])

    # Check first two tokens for deprecated command patterns like ['branch', 'next']
    # Only the first two tokens matter for compound deprecated commands
    handle_deprecated_command_names(click_input[:2])

    return click_input
