"""Scope specification for branch operations.

This module defines the scope specifications for branch traversal operations.
"""

from typing import TypedDict


class TScopeSpec(TypedDict, total=False):
    """Type for scope specification."""
    recursive_parents: bool
    current_branch: bool
    recursive_children: bool


class _ScopeConstants:
    """Constants for different scope types."""

    BRANCH: TScopeSpec = {
        "recursive_parents": False,
        "current_branch": True,
        "recursive_children": False,
    }

    DOWNSTACK: TScopeSpec = {
        "recursive_parents": True,
        "current_branch": True,
        "recursive_children": False,
    }

    STACK: TScopeSpec = {
        "recursive_parents": True,
        "current_branch": True,
        "recursive_children": True,
    }

    UPSTACK: TScopeSpec = {
        "recursive_parents": False,
        "current_branch": True,
        "recursive_children": True,
    }

    UPSTACK_EXCLUSIVE: TScopeSpec = {
        "recursive_parents": False,
        "current_branch": False,
        "recursive_children": True,
    }


SCOPE = _ScopeConstants()
