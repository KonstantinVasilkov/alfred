"""Test module for LLM connectors main entry point."""

from llm_connectors.main import main


def test_main_exists() -> None:
    """Test that main function exists and is callable."""
    assert callable(main)
