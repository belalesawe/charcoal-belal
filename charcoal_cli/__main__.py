"""Entry point for python -m charcoal_cli."""

import sys

from charcoal_cli.cli import main
from charcoal_cli.lib.pre_yargs.preprocess_command import get_click_input

if __name__ == "__main__":  # pragma: no cover
    # Preprocess command-line arguments before Click processes them
    # This handles:
    # - Git command passthrough (may exit)
    # - Shortcut expansion (e.g., 'bco' -> ['b', 'co'])
    # - Deprecated command checking (may exit)
    processed_args = get_click_input()

    # Invoke Click with processed arguments
    # Click expects sys.argv[0] to be the program name
    sys.argv = [sys.argv[0]] + processed_args
    main()
