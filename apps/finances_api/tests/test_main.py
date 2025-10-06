"""Test module for finances API main entry point."""

from finances_api.main import main


def test_main_exists() -> None:
    """Test that main function exists and is callable."""
    assert callable(main)
