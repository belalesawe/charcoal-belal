"""Generate random IDs for demo and testing purposes."""

import random
import string


def make_id(length: int) -> str:
    """Generate a random alphanumeric ID of the specified length.

    Args:
        length: Number of characters in the ID

    Returns:
        Random string of uppercase letters and digits
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
