"""GitRepo utility class for demo and testing purposes."""

import os
import subprocess
import sys
from pathlib import Path


class GitRepo:
    """Helper class for creating and managing git repositories for testing and demos."""

    def __init__(self, dir_path: str, existing_repo: bool = False, repo_url: str | None = None):
        """Initialize a GitRepo instance.

        Args:
            dir_path: Path to the repository directory
            existing_repo: If True, don't initialize a new repo
            repo_url: If provided, clone from this URL instead of initializing
        """
        self.dir = dir_path
        self.user_config_path = os.path.join(dir_path, '.git/.graphite_user_config')

        if existing_repo:
            return

        if repo_url:
            subprocess.run(['git', 'clone', repo_url, dir_path], check=True)
        else:
            subprocess.run(['git', 'init', dir_path, '-b', 'main'], check=True)

    def run_git_command(self, args: list[str]) -> None:
        """Run a git command in the repository directory.

        Args:
            args: Git command arguments (without 'git' prefix)
        """
        subprocess.run(
            ['git'] + args,
            cwd=self.dir,
            stdout=subprocess.DEVNULL if not os.environ.get('DEBUG') else None,
            stderr=subprocess.DEVNULL if not os.environ.get('DEBUG') else None,
        )

    def run_cli_command(self, command: list[str], cwd: str | None = None) -> None:
        """Run a charcoal CLI command in the repository directory.

        Args:
            command: CLI command arguments
            cwd: Working directory (defaults to self.dir)
        """
        # Get the path to the charcoal_cli module
        import charcoal_cli
        cli_module_path = Path(charcoal_cli.__file__).parent / '__main__.py'

        env = os.environ.copy()
        env['GRAPHITE_DISABLE_TELEMETRY'] = '1'
        env['GRAPHITE_DISABLE_UPGRADE_PROMPT'] = '1'
        env['GRAPHITE_DISABLE_SURVEY'] = '1'
        if 'GRAPHITE_PROFILE' in env:
            del env['GRAPHITE_PROFILE']

        result = subprocess.run(
            [sys.executable, str(cli_module_path)] + command,
            cwd=cwd or self.dir,
            env=env,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            error_msg = '\n'.join([
                f'Command failed with exit code {result.returncode}',
                'stdout:',
                result.stdout,
                'stderr:',
                result.stderr,
            ])
            raise RuntimeError(error_msg)

    def run_git_command_and_get_output(self, args: list[str]) -> str:
        """Run a git command and return its output.

        Args:
            args: Git command arguments (without 'git' prefix)

        Returns:
            Stripped stdout from the git command
        """
        result = subprocess.run(
            ['git'] + args,
            cwd=self.dir,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def create_change(self, text_value: str, prefix: str | None = None, unstaged: bool = False) -> None:
        """Create a file change in the repository.

        Args:
            text_value: Content to write to the file
            prefix: Optional prefix for the filename
            unstaged: If True, don't stage the file
        """
        filename = f"{prefix}_test.txt" if prefix else "test.txt"
        file_path = os.path.join(self.dir, filename)

        with open(file_path, 'w') as f:
            f.write(text_value)

        if not unstaged:
            self.run_git_command(['add', file_path])

    def create_change_and_commit(self, text_value: str, prefix: str | None = None) -> None:
        """Create a file change and commit it.

        Args:
            text_value: Content to write and use as commit message
            prefix: Optional prefix for the filename
        """
        self.create_change(text_value, prefix)
        self.run_git_command(['add', '.'])
        self.run_git_command(['commit', '-m', text_value])

    def checkout_branch(self, name: str) -> None:
        """Checkout an existing branch.

        Args:
            name: Branch name to checkout
        """
        self.run_git_command(['checkout', name])

    def create_and_checkout_branch(self, name: str) -> None:
        """Create and checkout a new branch.

        Args:
            name: Branch name to create
        """
        self.run_git_command(['checkout', '-b', name])

    def current_branch_name(self) -> str:
        """Get the current branch name.

        Returns:
            Name of the current branch
        """
        return self.run_git_command_and_get_output(['branch', '--show-current'])
