"""Utility functions for branch name manipulation.

This module provides functions for sanitizing branch names to ensure they
only contain supported characters.
"""

import re

from charcoal_cli.lib.context import TContext


# Regex patterns for branch name sanitization
# Matches any character that is NOT: hyphen, underscore, slash, dot, or alphanumeric
BRANCH_NAME_REPLACE_REGEX = re.compile(r"[^-_/.a-zA-Z0-9]+")
# Matches any trailing slash or dot characters
BRANCH_NAME_IGNORE_REGEX = re.compile(r"[/.]*$")


def get_branch_replacement(context: TContext) -> str:
    """Get the replacement character for unsupported characters in branch names.

    Args:
        context: Application context with user configuration

    Returns:
        The replacement character (defaults to underscore if not configured)
    """
    replacement = context.userConfig.data.branchReplacement
    return replacement if replacement is not None else "_"


def remove_unsupported_trailing_characters(input_str: str) -> str:
    """Remove unsupported trailing characters (slashes and dots) from a string.

    Args:
        input_str: The input string to clean

    Returns:
        The string with trailing slashes and dots removed
    """
    return BRANCH_NAME_IGNORE_REGEX.sub("", input_str)


def replace_unsupported_characters(input_str: str, context: TContext) -> str:
    """Replace unsupported characters in branch names with the configured replacement.

    This function sanitizes branch names by:
    1. Removing unsupported trailing characters (slashes and dots)
    2. Replacing any other unsupported characters with the user's configured
       replacement character (default: underscore)

    Supported characters are: hyphen, underscore, slash, dot, and alphanumeric

    Args:
        input_str: The input string to sanitize
        context: Application context with user configuration

    Returns:
        The sanitized string safe for use in branch names
    """
    # First remove unsupported trailing characters
    stripped_input = remove_unsupported_trailing_characters(input_str)
    
    # Then replace all other unsupported characters
    replacement = get_branch_replacement(context)
    return BRANCH_NAME_REPLACE_REGEX.sub(replacement, stripped_input)


def set_branch_prefix(new_prefix: str, context: TContext) -> str:
    """Set a new branch prefix after sanitizing it.

    Args:
        new_prefix: The new prefix to set
        context: Application context with user configuration

    Returns:
        The sanitized prefix that was actually stored
    """
    # Sanitize the prefix
    prefix = replace_unsupported_characters(new_prefix, context)
    
    # Update the configuration
    context.userConfig.update(lambda data: setattr(data, "branchPrefix", prefix))
    
    return prefix
