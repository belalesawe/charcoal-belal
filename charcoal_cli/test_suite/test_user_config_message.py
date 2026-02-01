"""Tests for user message configuration commands (submit_body, etc)."""

from click.testing import CliRunner

from charcoal_cli.cli import main


def test_submit_body_query_default():
    """Test querying submit-body when at default."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "submit-body"])
    assert result.exit_code == 0
    assert "PR body" in result.output or "commit messages" in result.output


def test_submit_body_enable():
    """Test enabling commit messages in PR body."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "submit-body", "--include-commit-messages"])
    assert result.exit_code == 0
    assert "include commit messages" in result.output


def test_submit_body_disable():
    """Test disabling commit messages in PR body."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "submit-body", "--no-include-commit-messages"])
    assert result.exit_code == 0
    assert "not include commit messages" in result.output


def test_branch_date_enable():
    """Test enabling branch date."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "branch-date", "--enable"])
    assert result.exit_code == 0
    assert "enabled" in result.output.lower()


def test_branch_date_disable():
    """Test disabling branch date."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "branch-date", "--disable"])
    assert result.exit_code == 0
    assert "disabled" in result.output.lower()


def test_branch_prefix_set():
    """Test setting branch prefix with sanitization."""
    runner = CliRunner()
    # Test with trailing slash - should be sanitized to "feature"
    result = runner.invoke(main, ["user", "branch-prefix", "--set", "feature/"])
    assert result.exit_code == 0
    # The sanitized value (without trailing slash) should be shown
    assert "feature" in result.output
    assert result.output.strip().endswith('"feature"') or result.output.strip().endswith('"feature"\n')


def test_branch_prefix_set_with_special_chars():
    """Test that branch prefix sanitizes special characters."""
    runner = CliRunner()
    # Test with special characters - should be replaced with underscore
    result = runner.invoke(main, ["user", "branch-prefix", "--set", "my@feature#"])
    assert result.exit_code == 0
    # Special chars should be replaced
    assert "my_feature" in result.output


def test_branch_replacement_set():
    """Test setting branch replacement pattern."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "branch-replacement", "--set-underscore"])
    assert result.exit_code == 0
    assert "underscore" in result.output


def test_restack_date_enable():
    """Test enabling restack date."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "restack-date", "--use-author-date"])
    assert result.exit_code == 0
    assert "committer-date-is-author-date" in result.output


def test_restack_date_disable():
    """Test disabling restack date."""
    runner = CliRunner()
    result = runner.invoke(main, ["user", "restack-date", "--no-use-author-date"])
    assert result.exit_code == 0
    assert "will not" in result.output
