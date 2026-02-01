"""Pytest configuration and fixtures for charcoal-cli tests."""

import pytest


@pytest.fixture
def mock_context():
    """Create a mock context for testing."""
    from charcoal_cli.lib.context import create_context

    return create_context()
