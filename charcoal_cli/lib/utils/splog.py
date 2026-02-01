"""Simple logging utilities for command-line output.

This module provides basic logging functions with colored output,
matching the TypeScript chalk-based splog implementation.
"""


def error(message: str) -> None:
    """Print an error message to stdout with red color.

    Matches the TypeScript composeSplog().error() behavior which uses
    chalk.redBright for the entire message including the "ERROR: " prefix.

    Args:
        message: Error message to display
    """
    red_bright = "\033[91m"  # ANSI bright red (equivalent to chalk.redBright)
    reset = "\033[0m"  # ANSI reset
    print(f"{red_bright}ERROR: {message}{reset}")


def warn(message: str) -> None:
    """Print a warning message to stdout with yellow color.

    Matches the TypeScript composeSplog().warn() behavior which uses
    chalk.yellow for the entire message including the "WARNING: " prefix.

    Args:
        message: Warning message to display
    """
    yellow = "\033[33m"  # ANSI yellow (equivalent to chalk.yellow)
    reset = "\033[0m"  # ANSI reset
    print(f"{yellow}WARNING: {message}{reset}")


def info(message: str) -> None:
    """Print an info message to stdout.

    Args:
        message: Info message to display
    """
    print(message)


def debug(_message: str) -> None:
    """Print a debug message (no-op by default).

    Args:
        _message: Debug message to display (unused in stub implementation)
    """
    # Debug messages are typically suppressed unless debug mode is enabled
    pass
