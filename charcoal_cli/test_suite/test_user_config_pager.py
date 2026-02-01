"""Tests for user pager configuration command."""

from click.testing import CliRunner

from charcoal_cli.cli import main


def test_pager_query_default():
    """Test querying pager when not set."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "pager"])
    assert result.exit_code == 0
    # Should show either "not set" or current git pager
    assert "pager" in result.output.lower()


def test_pager_set():
    """Test setting pager."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "pager", "--set", "less -FRX"])
    assert result.exit_code == 0
    assert "less" in result.output


def test_pager_disable():
    """Test disabling pager."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "pager", "--disable"])
    assert result.exit_code == 0
    assert "disabled" in result.output.lower()


def test_pager_unset():
    """Test unsetting pager."""
    runner = CliRunner()
    # First set a pager
    runner.invoke(main, ["user", "pager", "--set", "less"])
    # Then unset it
    result = runner.invoke(main, ["user", "pager", "--unset"])
    assert result.exit_code == 0
    assert "erased" in result.output.lower() or "defaulting" in result.output.lower()
