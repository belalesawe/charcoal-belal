"""Configuration management for Charcoal CLI.

This module provides the ConfigManager class for loading and saving configuration
files, with support for both user-level and repository-level configurations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Generic, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ConfigManager(Generic[T]):
    """Manager for loading and saving configuration files."""

    def __init__(self, config_path: Path, model_class: Type[T]):
        """Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file
            model_class: Pydantic model class for the configuration
        """
        self.config_path = config_path
        self.model_class = model_class
        self._data: T | None = None

    @property
    def data(self) -> T:
        """Get the configuration data, loading it if necessary.

        Returns:
            The configuration model instance
        """
        if self._data is None:
            self._data = self.load()
        return self._data

    def load(self) -> T:
        """Load configuration from the file.

        If the file doesn't exist, returns a new instance with defaults.

        Returns:
            The configuration model instance
        """
        if not self.config_path.exists():
            return self.model_class()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return self.model_class(**data)
        except (json.JSONDecodeError, ValueError):
            # If file is corrupted, return defaults
            return self.model_class()

    def save(self, data: T) -> None:
        """Save configuration to the file.

        Args:
            data: The configuration model instance to save
        """
        # Ensure the directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict and save
        config_dict = data.model_dump(by_alias=True, exclude_none=False)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=2)
            f.write("\n")  # Add trailing newline

        # Update cached data
        self._data = data

    def update(self, updater: Callable[[T], None]) -> None:
        """Update configuration using a callback function.

        Args:
            updater: Function that modifies the configuration data in place
        """
        data = self.data
        updater(data)
        self.save(data)


def get_user_config_path() -> Path:
    """Get the path to the user configuration file.

    Returns:
        Path to ~/.graphite/user_config.json
    """
    home = Path.home()
    return home / ".graphite" / "user_config.json"


def get_repo_config_path() -> Path | None:
    """Get the path to the repository configuration file.

    Returns:
        Path to .git/.graphite/repo_config.json if in a git repository,
        None otherwise
    """
    # Try to find the .git directory
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        git_dir = parent / ".git"
        if git_dir.exists():
            return git_dir / ".graphite" / "repo_config.json"
    return None
