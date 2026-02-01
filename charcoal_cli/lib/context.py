"""Context object for sharing state across commands and actions."""

from typing import Any, Protocol

from charcoal_cli.lib.config_manager import ConfigManager, get_user_config_path
from charcoal_cli.lib.config_models import UserConfig


class Engine(Protocol):
    """Protocol for the engine interface."""

    @property
    def current_branch_precondition(self) -> str:
        """Get the current branch, raising an error if not available."""
        ...

    @property
    def current_branch(self) -> str | None:
        """Get the current branch or None."""
        ...

    @property
    def trunk(self) -> str:
        """Get the trunk branch name."""
        ...

    @property
    def all_branch_names(self) -> list[str]:
        """Get all branch names in the repository."""
        ...

    def get_relative_stack(self, branch: str, scope: Any) -> list[str]:
        """Get branches in the relative stack based on scope."""
        ...

    def is_trunk(self, branch: str) -> bool:
        """Check if a branch is a trunk branch."""
        ...

    def is_branch_tracked(self, branch: str) -> bool:
        """Check if a branch is tracked by Charcoal."""
        ...

    def is_branch_fixed(self, branch: str) -> bool:
        """Check if a branch is fixed (doesn't need restacking)."""
        ...

    def checkout_branch(self, branch: str) -> None:
        """Checkout the specified branch."""
        ...

    def set_parent(self, branch: str, parent: str) -> None:
        """Set the parent of a branch."""
        ...

    def get_parent(self, branch: str) -> str | None:
        """Get the parent branch of the specified branch."""
        ...

    def get_parent_precondition(self, branch: str) -> str:
        """Get the parent branch, raising an error if not available."""
        ...

    def get_children(self, branch: str) -> list[str] | None:
        """Get the children branches of the specified branch."""
        ...

    def log_long(self) -> None:
        """Display a long format git log with branch relationships."""
        ...


class SpLog(Protocol):
    """Protocol for logging interface."""

    def info(self, message: str) -> None:
        """Log an info message."""
        ...

    def error(self, message: str) -> None:
        """Log an error message."""
        ...

    def debug(self, message: str) -> None:
        """Log a debug message."""
        ...

    def page(self, message: str) -> None:
        """Display a message with paging for long content."""
        ...


class TContext:
    """Context object providing access to shared resources."""

    def __init__(
        self,
        engine: Engine,
        splog: SpLog,
        user_config: ConfigManager[UserConfig] | None = None,
        prompts: Any = None,
    ):
        self.engine = engine
        self.splog = splog
        self.userConfig = user_config or ConfigManager(
            get_user_config_path(), UserConfig
        )
        self.prompts = prompts or self._default_prompts

    async def _default_prompts(self, config: dict[str, Any]) -> dict[str, Any]:
        """Default prompts implementation for stub/testing.

        Args:
            config: Prompt configuration

        Returns:
            Dictionary with prompt results
        """
        # Stub implementation returns the initial choice or first choice
        choices = config.get("choices", [])
        initial = config.get("initial", 0)
        name = config.get("name", "value")

        if choices and 0 <= initial < len(choices):
            return {name: choices[initial]["value"]}
        elif choices:
            return {name: choices[0]["value"]}
        else:
            return {name: ""}


# Stub implementations for testing and development
class StubEngine:
    """Stub implementation of Engine for development."""

    @property
    def current_branch_precondition(self) -> str:
        return "main"

    @property
    def current_branch(self) -> str | None:
        return "main"

    @property
    def trunk(self) -> str:
        return "main"

    @property
    def all_branch_names(self) -> list[str]:
        return ["main", "feature-a", "feature-b"]

    def get_relative_stack(self, branch: str, scope: Any) -> list[str]:
        _ = scope  # Unused in stub
        return [branch]

    def is_trunk(self, branch: str) -> bool:
        return branch in ("main", "master", "trunk")

    def is_branch_tracked(self, branch: str) -> bool:
        """Check if a branch is tracked."""
        return branch in ("feature-a", "feature-b")

    def is_branch_fixed(self, branch: str) -> bool:
        """Check if a branch is fixed."""
        return True

    def checkout_branch(self, branch: str) -> None:
        _ = branch  # Unused in stub

    def set_parent(self, branch: str, parent: str) -> None:
        _ = (branch, parent)  # Unused in stub

    def get_parent(self, branch: str) -> str | None:
        """Get parent branch."""
        if branch == "feature-a":
            return "main"
        elif branch == "feature-b":
            return "feature-a"
        return None

    def get_parent_precondition(self, branch: str) -> str:
        """Get parent branch with precondition."""
        parent = self.get_parent(branch)
        if parent is None:
            return "main"
        return parent

    def get_children(self, branch: str) -> list[str] | None:
        """Get children branches."""
        if branch == "main":
            return ["feature-a"]
        elif branch == "feature-a":
            return ["feature-b"]
        return None

    def log_long(self) -> None:
        """Display long format log."""
        print("Git log (long format) - stub implementation")


class StubSpLog:
    """Stub implementation of SpLog for development."""

    def info(self, message: str) -> None:
        print(message)

    def error(self, message: str) -> None:
        print(f"ERROR: {message}")

    def debug(self, message: str) -> None:
        """Log debug message."""
        # In stub, we can just print it or suppress it
        pass

    def page(self, message: str) -> None:
        """Page message - in stub just print it."""
        print(message)


def create_context(user_config: ConfigManager[UserConfig] | None = None) -> TContext:
    """Create a context with stub implementations.

    Args:
        user_config: Optional user config manager (creates default if not provided)

    Returns:
        Context object with stub implementations
    """
    return TContext(StubEngine(), StubSpLog(), user_config)
