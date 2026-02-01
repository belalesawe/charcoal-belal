"""Configuration models using Pydantic.

This module defines Pydantic models for user and repository configuration,
providing validation and type safety for configuration data.
"""

from __future__ import annotations

import os
import subprocess
from typing import Optional

from pydantic import BaseModel, Field


class UserConfig(BaseModel):
    """User configuration model for Charcoal CLI.

    This configuration is stored in ~/.graphite/user_config.json and persists
    across all repositories.
    """

    editor: Optional[str] = Field(
        default=None, description="Default editor for Charcoal operations"
    )
    pager: Optional[str] = Field(
        default=None, description="Default pager for Charcoal output"
    )
    tips: bool = Field(default=True, description="Show usage tips in CLI output")
    branchDate: Optional[bool] = Field(
        default=None,
        description="Prepend date to auto-generated branch names",
        alias="branch_date",
    )
    branchPrefix: Optional[str] = Field(
        default=None,
        description="Prefix for auto-generated branch names",
        alias="branch_prefix",
    )
    branchReplacement: Optional[str] = Field(
        default=None,
        description="Replacement pattern for branch names",
        alias="branch_replacement",
    )
    restackCommitterDateIsAuthorDate: Optional[bool] = Field(
        default=None,
        description="Set committer date to author date during restack",
        alias="restack_committer_date_is_author_date",
    )
    submitIncludeCommitMessages: Optional[bool] = Field(
        default=None,
        description="Include commit messages in PR descriptions",
        alias="submit_include_commit_messages",
    )

    model_config = {
        "populate_by_name": True,  # Allow both snake_case and camelCase field names
    }

    def get_editor(self) -> str:
        """Get the editor, falling back to git config and environment variables.

        Returns:
            The editor command to use
        """
        if self.editor:
            return self.editor

        # Fall back to git config
        try:
            result = subprocess.run(
                ["git", "config", "--global", "core.editor"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Fall back to environment variables
        editor = os.environ.get("GIT_EDITOR") or os.environ.get("EDITOR") or "vi"
        return editor

    def get_pager(self) -> Optional[str]:
        """Get the pager, falling back to git config and environment variables.

        Returns:
            The pager command to use, or None if pager is disabled
        """
        # Empty string means pager is explicitly disabled
        if self.pager == "":
            return None

        if self.pager:
            return self.pager

        # Fall back to git config
        try:
            result = subprocess.run(
                ["git", "config", "--global", "core.pager"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Fall back to environment variables
        pager = os.environ.get("GIT_PAGER") or os.environ.get("PAGER")
        return pager


class RepoConfig(BaseModel):
    """Repository-specific configuration model.

    This configuration is stored in .git/.graphite/repo_config.json and is
    specific to each repository.
    """

    default_stack_base: Optional[str] = Field(
        default=None, description="Default base branch for stacks"
    )
