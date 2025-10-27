"""Observability middleware and helper utilities."""

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import structlog

T = TypeVar("T", bound=Callable[..., Any])


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structlog logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured structlog logger

    Example:
        ```python
        logger = get_logger(__name__)
        logger.info("user_action", user_id=123, action="login")
        ```

    """
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    """Bind context variables that will be included in all subsequent logs.

    Args:
        **kwargs: Key-value pairs to bind to logging context

    Example:
        ```python
        bind_context(user_id=123, session_id="abc")
        logger.info("event")  # Will include user_id and session_id
        ```

    """
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    """Clear all bound context variables."""
    structlog.contextvars.clear_contextvars()


def log_with_fingerprint(
    logger: structlog.stdlib.BoundLogger,
    level: str,
    message: str,
    fingerprint: list[str],
    **kwargs: Any,
) -> None:
    """Log a message with Sentry fingerprinting to prevent duplicate issues.

    Args:
        logger: structlog logger instance
        level: Log level (info, warning, error, exception)
        message: Log message
        fingerprint: List of strings for Sentry fingerprinting
        **kwargs: Additional structured data

    Example:
        ```python
        log_with_fingerprint(
            logger, "error", "llm_processing_failed", fingerprint=["llm-timeout"], user_id=123, error_type="timeout"
        )
        ```

        This ensures all LLM timeout errors group as ONE issue in Sentry,
        instead of creating separate issues per user.

    """
    log_method = getattr(logger, level)
    kwargs["extra"] = {"sentry_fingerprint": fingerprint}
    log_method(message, **kwargs)


# Convenience functions for common patterns


def log_user_error(
    logger: structlog.stdlib.BoundLogger,
    error_type: str,
    user_id: int | str,
    **kwargs: Any,
) -> None:
    """Log a user-facing error with proper fingerprinting.

    Args:
        logger: structlog logger instance
        error_type: Type of error (e.g., "validation_failed", "rate_limited")
        user_id: User identifier
        **kwargs: Additional context

    Example:
        ```python
        log_user_error(logger, "rate_limited", user_id=123, limit=10, window="1min")
        ```

    """
    log_with_fingerprint(
        logger,
        "warning",
        "user_error",
        fingerprint=["user-error", error_type],
        user_id=user_id,
        error_type=error_type,
        **kwargs,
    )


def log_integration_error(
    logger: structlog.stdlib.BoundLogger,
    integration: str,
    error_type: str,
    **kwargs: Any,
) -> None:
    """Log an external integration error with proper fingerprinting.

    Args:
        logger: structlog logger instance
        integration: Name of external service (e.g., "anthropic", "telegram")
        error_type: Type of error (e.g., "timeout", "unauthorized")
        **kwargs: Additional context

    Example:
        ```python
        log_integration_error(logger, "anthropic", "timeout", model="claude-3-haiku", request_id="abc123")
        ```

    """
    log_with_fingerprint(
        logger,
        "error",
        "integration_error",
        fingerprint=["integration-error", integration, error_type],
        integration=integration,
        error_type=error_type,
        **kwargs,
    )


def logged_function(logger: structlog.stdlib.BoundLogger) -> Callable[[T], T]:
    """Automatically log function calls with timing.

    Args:
        logger: structlog logger instance

    Returns:
        Decorator function

    Example:
        ```python
        logger = get_logger(__name__)


        @logged_function(logger)
        async def process_message(user_id: int, message: str) -> str:
            # Function implementation
            return result
        ```

        Logs:
        - function_called: When function starts
        - function_completed: When function completes successfully
        - function_failed: When function raises exception

    """

    def decorator(func: T) -> T:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__  # type: ignore[attr-defined]
            logger.info(
                "function_called",
                function=func_name,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            try:
                result = await func(*args, **kwargs)  # type: ignore[misc]
                logger.info("function_completed", function=func_name)
                return result
            except Exception as e:
                logger.exception(
                    "function_failed",
                    function=func_name,
                    error_type=type(e).__name__,
                    extra={"sentry_fingerprint": [f"function-error-{func_name}"]},
                )
                raise

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__  # type: ignore[attr-defined]
            logger.info(
                "function_called",
                function=func_name,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            try:
                result = func(*args, **kwargs)  # type: ignore[misc]
                logger.info("function_completed", function=func_name)
                return result
            except Exception as e:
                logger.exception(
                    "function_failed",
                    function=func_name,
                    error_type=type(e).__name__,
                    extra={"sentry_fingerprint": [f"function-error-{func_name}"]},
                )
                raise

        # Return appropriate wrapper based on whether function is async
        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore[return-value]
        return sync_wrapper  # type: ignore[return-value]

    return decorator


# Example usage patterns (for documentation)

"""
## Structlog Usage Examples

### 1. Basic Structured Logging
```python
from shared_infra.observability_middleware import get_logger

logger = get_logger(__name__)
logger.info("user_login", user_id=123, ip="1.2.3.4")
logger.warning("slow_query", query_time_ms=1500, table="users")
```

### 2. Context Binding (Automatic Field Inclusion)
```python
from shared_infra.observability_middleware import bind_context, clear_context

# Bind context at request start
bind_context(user_id=123, session_id="abc")

logger.info("action_started")  # Includes user_id and session_id
logger.info("action_completed")  # Also includes user_id and session_id

# Clear context when done
clear_context()
```

### 3. Sentry Fingerprinting (Prevent Duplicate Issues)
```python
from shared_infra.observability_middleware import log_with_fingerprint

# Without fingerprinting: 100 users = 100 Sentry issues
# With fingerprinting: 100 users = 1 Sentry issue

log_with_fingerprint(
    logger,
    "error",
    "llm_timeout",
    fingerprint=["llm-timeout"],
    user_id=user_id,
    model="claude-3-haiku"
)
```

### 4. Exception Logging
```python
try:
    result = await api_call()
except TimeoutError as e:
    logger.exception(
        "api_timeout",
        service="anthropic",
        extra={"sentry_fingerprint": ["api-timeout"]}
    )
```

### 5. Integration Error Logging
```python
from shared_infra.observability_middleware import log_integration_error

log_integration_error(
    logger,
    "telegram",
    "send_message_failed",
    chat_id=123,
    error_code=429
)
```
"""
