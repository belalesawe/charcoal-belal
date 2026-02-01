"""Handle deprecated command names with appropriate warnings and errors.

This module checks for deprecated command names and aliases, showing
migration messages to users and exiting with errors where appropriate.
"""

import sys

from charcoal_cli.lib.utils import splog


NAV_WARNING = "\n".join([
    "The `branch` commands `next` and `previous` (aka `bn` and `bp`) have been renamed.",
    "Please use `up` and `down` (aka `bu` and `bd`) respectively.",
])

INFO_WARNING = "\n".join([
    "The `branch` command `show` has been renamed.",
    "Please use `info` (aka `gt bi`).",
])

GET_WARNING = "\n".join([
    "The `downstack` command `sync` has been renamed.",
    "Please use `get` (aka `gt dsg`).",
])

FIX_WARNING = "\n".join([
    "The `upstack` and `stack` command `fix` has been renamed.",
    "Please use `restack` (aka `gt sr`/`gt usr`).",
    "The `fix`/`f` alias will be removed in an upcoming version.",
])


def handle_deprecated_command_names(command: list[str]) -> None:
    """Check for deprecated command names and handle them appropriately.

    Some deprecated commands cause an error exit (like branch next/previous),
    while others show a warning but continue (like fix alias for restack).

    Args:
        command: List of command tokens (e.g., ['branch', 'next'])
    """
    if len(command) == 0:
        return

    first_cmd = command[0]
    second_cmd = command[1] if len(command) > 1 else None

    # Branch command deprecations
    if first_cmd in ("branch", "b"):
        if second_cmd in ("next", "n", "previous", "p"):
            splog.error(NAV_WARNING)
            sys.exit(1)

        if second_cmd == "show":
            splog.error(INFO_WARNING)
            sys.exit(1)

    # Downstack command deprecations
    elif first_cmd in ("downstack", "ds"):
        if second_cmd == "sync":
            splog.error(GET_WARNING)
            sys.exit(1)

    # Upstack/stack command deprecations (warning only, not error)
    elif first_cmd in ("upstack", "us", "stack", "s"):
        if second_cmd in ("fix", "f"):
            splog.warn(FIX_WARNING)
