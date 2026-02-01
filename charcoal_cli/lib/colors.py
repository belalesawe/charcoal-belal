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


# ANSI reset code
RESET = "\033[0m"
