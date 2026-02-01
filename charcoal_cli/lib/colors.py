"""Color constants for terminal output.

This module provides color definitions used in log visualization and other
terminal output. The colors are defined as RGB tuples compatible with ANSI
color codes.
"""

from typing import Tuple

# RGB color tuples for graphite log visualization
# These colors are used in a cycling pattern for branch visualization
GRAPHITE_COLORS: list[Tuple[int, int, int]] = [
    (76, 203, 241),   # Cyan
    (77, 202, 125),   # Green
    (110, 173, 38),   # Olive
    (245, 200, 0),    # Yellow
    (248, 144, 72),   # Orange
    (244, 98, 81),    # Red-orange
    (235, 130, 188),  # Pink
    (159, 131, 228),  # Purple
    (80, 132, 243),   # Blue
]


def rgb_to_ansi(r: int, g: int, b: int) -> str:
    """Convert RGB values to ANSI escape code.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        ANSI escape code string for the color
    """
    return f"\033[38;2;{r};{g};{b}m"


def get_log_short_color(index: int) -> str:
    """Get ANSI color code for log short visualization.

    Colors cycle through GRAPHITE_COLORS array based on index.
    Every 2 indices uses the same color.

    Args:
        index: Position index for color selection

    Returns:
        ANSI escape code for the color
    """
    color_index = (index // 2) % len(GRAPHITE_COLORS)
    r, g, b = GRAPHITE_COLORS[color_index]
    return rgb_to_ansi(r, g, b)


# Additional ANSI color codes
RESET = "\033[0m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"


def get_branch_color(branch_name: str, context) -> str:
    """Get color for a branch based on its status.

    Args:
        branch_name: Name of the branch
        context: Application context with engine

    Returns:
        ANSI color escape sequence
    """
    # Current branch is cyan
    if hasattr(context, 'engine') and context.engine.current_branch == branch_name:
        return CYAN

    # Untracked branches are yellow
    if hasattr(context, 'engine') and hasattr(context.engine, 'is_branch_tracked'):
        if not context.engine.is_branch_tracked(branch_name):
            return YELLOW

    return ""
