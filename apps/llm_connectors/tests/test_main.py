"""Test module for LLM connectors main entry point."""


def test_main_exists() -> None:
    """Test that main function exists and is callable."""
    from llm_connectors.main import main

    assert callable(main)
