"""Tests for CLI commands."""

from click.testing import CliRunner

from charcoal_cli.cli import main


def test_cli_help():
    """Test that CLI help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "charcoal CLI" in result.output


def test_upstack_help():
    """Test that upstack help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["upstack", "--help"])
    assert result.exit_code == 0
    assert "upstack" in result.output.lower()


def test_downstack_help():
    """Test that downstack help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["downstack", "--help"])
    assert result.exit_code == 0
    assert "downstack" in result.output.lower()


def test_stack_help():
    """Test that stack help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["stack", "--help"])
    assert result.exit_code == 0
    assert "stack" in result.output.lower()


def test_upstack_onto_help():
    """Test that upstack onto help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["upstack", "onto", "--help"])
    assert result.exit_code == 0
    assert "onto" in result.output.lower()


def test_upstack_test_help():
    """Test that upstack test help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["upstack", "test", "--help"])
    assert result.exit_code == 0
    assert "command" in result.output.lower()


def test_downstack_get_help():
    """Test that downstack get help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["downstack", "get", "--help"])
    assert result.exit_code == 0
    assert "get" in result.output.lower()


def test_downstack_test_help():
    """Test that downstack test help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["downstack", "test", "--help"])
    assert result.exit_code == 0
    assert "command" in result.output.lower()


def test_downstack_track_help():
    """Test that downstack track help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["downstack", "track", "--help"])
    assert result.exit_code == 0
    assert "track" in result.output.lower()


def test_stack_test_help():
    """Test that stack test help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["stack", "test", "--help"])
    assert result.exit_code == 0
    assert "command" in result.output.lower()
