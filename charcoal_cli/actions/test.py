"""Action to run tests on branches in a stack.

This action executes a user-specified shell command on each branch in a scope
(upstack, downstack, or full stack) and displays results with status indicators
and timing information.
"""

import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, Literal, Optional

from charcoal_cli.lib.context import TContext
from charcoal_cli.lib.engine.scope_spec import SCOPE, TScopeSpec


TestStatus = Literal["[pending]", "[success]", "[failed]", "[running]", "[killed]"]


class TestState:
    """State for a single branch test."""

    def __init__(self):
        self.status: TestStatus = "[pending]"
        self.duration: Optional[float] = None
        self.outfile: Optional[str] = None


def test_stack(opts: dict, context: TContext) -> None:
    """Run tests on branches in a stack.

    Args:
        opts: Options including:
            - scope: TScopeSpec defining which branches to test
            - includeTrunk: Whether to include trunk branches
            - command: Shell command to run on each branch
        context: The application context
    """
    scope: TScopeSpec = opts["scope"]
    include_trunk: bool = opts.get("includeTrunk", False)
    command: str = opts["command"]

    current_branch = context.engine.current_branch_precondition

    # Get branches to test using the provided scope
    # This allows upstack/downstack/stack test commands to operate on different branch sets
    branches = context.engine.get_relative_stack(current_branch, scope)
    if not include_trunk:
        branches = [b for b in branches if not context.engine.is_trunk(b)]

    # Initialize state for each branch
    state: Dict[str, TestState] = {}
    for branch in branches:
        state[branch] = TestState()

    # Create a temp output directory for debugging
    tmp_dir = tempfile.mkdtemp(prefix="charcoal-test-")

    # Kick off the testing
    log_state(state, False, context)
    for branch_name in branches:
        test_branch(
            branch_name=branch_name,
            command=command,
            tmp_dir_name=tmp_dir,
            state=state,
            context=context,
        )

    context.splog.info(f"Output files: {tmp_dir}")

    # Restore the original branch
    context.engine.checkout_branch(current_branch)


def test_branch(
    branch_name: str,
    command: str,
    tmp_dir_name: str,
    state: Dict[str, TestState],
    context: TContext,
) -> None:
    """Test a single branch.

    Args:
        branch_name: Name of the branch to test
        command: Shell command to execute
        tmp_dir_name: Directory for output files
        state: Shared state dictionary
        context: The application context
    """
    context.engine.checkout_branch(branch_name)

    # Create output file path (sanitize branch name for filesystem)
    output_path = Path(tmp_dir_name) / branch_name.replace("/", "-")

    # Mark the branch as running
    state[branch_name].status = "[running]"
    log_state(state, True, context)

    start_time = time.time()

    try:
        # Run the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

        # Write output to file
        output_path.write_text(result.stdout + result.stderr)

        if result.returncode == 0:
            state[branch_name].status = "[success]"
        else:
            state[branch_name].status = "[failed]"
            # Also write the return code
            with output_path.open("a") as f:
                f.write(f"\nExit code: {result.returncode}\n")

    except subprocess.TimeoutExpired:
        state[branch_name].status = "[killed]"
        output_path.write_text("Command timed out\n")
    except KeyboardInterrupt:
        state[branch_name].status = "[killed]"
        output_path.write_text("Command interrupted by user\n")
        raise
    except Exception as e:
        state[branch_name].status = "[failed]"
        output_path.write_text(f"Error: {str(e)}\n")

    state[branch_name].duration = time.time() - start_time
    state[branch_name].outfile = str(output_path)

    # Log updated state
    log_state(state, True, context)


def log_state(
    state: Dict[str, TestState], refresh: bool, context: TContext
) -> None:
    """Log the current test state.

    Args:
        state: Dictionary of branch states
        refresh: If True, move cursor up to overwrite previous output
        context: The application context
    """
    if refresh:
        # Move cursor up to overwrite previous output
        # Using ANSI escape codes
        num_lines = len(state)
        sys.stdout.write(f"\033[{num_lines}A")

    for branch_name, branch_state in state.items():
        # Clear the line
        sys.stdout.write("\033[2K")

        # Choose color based on status
        if branch_state.status in ("[failed]", "[killed]"):
            color_code = "\033[91m"  # Red
        elif branch_state.status == "[success]":
            color_code = "\033[92m"  # Green
        elif branch_state.status == "[running]":
            color_code = "\033[96m"  # Cyan
        else:
            color_code = "\033[90m"  # Gray

        reset_code = "\033[0m"

        # Format duration as HH:MM:SS
        duration_str = ""
        if branch_state.duration is not None:
            duration_seconds = int(branch_state.duration)
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60
            duration_str = f" ({hours:02d}:{minutes:02d}:{seconds:02d})"

        # Print the line
        message = f"- {color_code}{branch_state.status}{reset_code}: {branch_name}{duration_str}"
        context.splog.info(message)
