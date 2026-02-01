"""Pre-processing utilities for command-line arguments.

This package contains utilities that run before Click processes arguments,
including deprecated command warnings and git passthrough functionality.
"""

from charcoal_cli.lib.pre_yargs.preprocess_command import get_click_input

__all__ = ["get_click_input"]
