"""Tests for user editor configuration command."""

import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from charcoal_cli.cli import main
from charcoal_cli.lib.config_manager import ConfigManager
from charcoal_cli.lib.config_models import UserConfig


@pytest.fixture
def temp_config_file(monkeypatch):
    """Create a temporary config file for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "user_config.json"
        monkeypatch.setenv("HOME", tmpdir)
        yield config_path


def test_editor_query_default():
    """Test querying editor."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "editor"])
    assert result.exit_code == 0
    # Should show some output about the editor
    assert result.output.strip()


def test_editor_set():
    """Test setting editor."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "editor", "--set", "vim"])
    assert result.exit_code == 0
    assert "vim" in result.output


def test_editor_unset():
    """Test unsetting editor."""
    runner = CliRunner()
    # First set an editor
    runner.invoke(main, ["user", "editor", "--set", "vim"])
    # Then unset it
    result = runner.invoke(main, ["user", "editor", "--unset"])
    assert result.exit_code == 0
    assert "erased" in result.output.lower() or "defaulting" in result.output.lower()


def test_editor_query_after_set():
    """Test querying editor after setting it."""
    runner = CliRunner()
    # Set editor
    runner.invoke(main, ["user", "editor", "--set", "nano"])
    # Query it
    result = runner.invoke(main, ["user", "editor"])
    assert result.exit_code == 0
    assert "nano" in result.output
