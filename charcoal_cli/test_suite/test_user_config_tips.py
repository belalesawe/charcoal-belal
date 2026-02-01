"""Tests for user tips configuration command."""

from click.testing import CliRunner

from charcoal_cli.cli import main


def test_tips_query_default():
    """Test querying tips when at default."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "tips"])
    assert result.exit_code == 0
    assert "tips" in result.output.lower()
    assert ("enabled" in result.output.lower()) or ("disabled" in result.output.lower())


def test_tips_enable():
    """Test enabling tips."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "tips", "--enable"])
    assert result.exit_code == 0
    assert "enabled" in result.output.lower()


def test_tips_disable():
    """Test disabling tips."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "tips", "--disable"])
    assert result.exit_code == 0
    assert "disabled" in result.output.lower()


def test_tips_query_after_enable():
    """Test querying tips after enabling."""
    runner = CliRunner()
    # Enable tips
    runner.invoke(main, ["user", "tips", "--enable"])
    # Query it
    result = runner.invoke(main, ["user", "tips"])
    assert result.exit_code == 0
    assert "enabled" in result.output.lower()
