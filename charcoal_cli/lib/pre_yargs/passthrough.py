"""Pass through certain git commands directly to the git binary.

This module allows users to run common git commands through the charcoal CLI
as a convenience (e.g., `gt push` instead of `git push`).
"""

import subprocess
import sys


# Allowlist of git commands that can be passed through
GIT_COMMAND_ALLOWLIST = [
    "add",
    "am",
    "apply",
    "archive",
    "bisect",
    "blame",
    "bundle",
    "cherry-pick",
    "clean",
    "clone",
    "diff",
    "difftool",
    "fetch",
    "format-patch",
    "fsck",
    "grep",
    "merge",
    "mv",
    "notes",
    "pull",
    "push",
    "range-diff",
    "rebase",
    "reflog",
    "remote",
    "request-pull",
    "reset",
    "restore",
    "revert",
    "rm",
    "show",
    "send-email",
    "sparse-checkout",
    "stash",
    "status",
    "submodule",
    "switch",
    "tag",
]


def passthrough(args: list[str]) -> None:
    """Check if command should be passed through to git and execute if so.

    If the first argument after the program name matches an allowlisted git
    command, this function prints an informational message, runs the git
    command with inherited stdio, and exits with the git command's exit code.

    Args:
        args: Full command-line arguments including program name (sys.argv)
    """
    # Need at least 2 args: [program_name, command, ...]
    # For Python module: ['__main__.py', 'push', 'origin', 'main']
    # For installed binary: ['gt', 'push', 'origin', 'main']
    if len(args) <= 1:
        return

    command = args[1]
    if command not in GIT_COMMAND_ALLOWLIST:
        return

    # Build the git command string for display
    git_args = args[1:]
    git_command_str = " ".join(git_args)

    # Print informational message (using grey color code similar to chalk.grey)
    grey = "\033[90m"  # ANSI grey
    yellow = "\033[33m"  # ANSI yellow
    reset = "\033[0m"  # ANSI reset

    print(
        f"{grey}Passing command through to git...\n"
        f'Running: "{yellow}git {git_command_str}{grey}"\n{reset}',
        file=sys.stderr,
    )

    # Execute git command with inherited stdio (for interactive commands, colors, etc.)
    # Explicitly pass None for stdin, stdout, stderr to inherit from parent process
    # This matches TypeScript's { stdio: 'inherit' } behavior
    result = subprocess.run(
        ["git"] + git_args,
        stdin=None,
        stdout=None,
        stderr=None,
    )

    # Exit with git's exit code (defensive null check matches TypeScript's `?? 0`)
    sys.exit(result.returncode if result.returncode is not None else 0)
