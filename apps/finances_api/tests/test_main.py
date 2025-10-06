"""Test module for finances API main entry point."""


def test_main_exists() -> None:
    """Test that main function exists and is callable."""
    from finances_api.main import main

    assert callable(main)
