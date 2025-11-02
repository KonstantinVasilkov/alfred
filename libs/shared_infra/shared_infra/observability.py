"""Observability setup: structured logging, OpenTelemetry, and Sentry integration."""

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any

import sentry_sdk
import structlog
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sentry_sdk.integrations.logging import LoggingIntegration

from shared_infra.config_base import BaseAppSettings


def setup_logging(settings: BaseAppSettings) -> None:
    """Configure structlog with environment-aware processors.

    Args:
        settings: Application settings with logging configuration

    """
    # Configure stdlib logging
    log_level = getattr(logging, settings.LOG_LEVEL.upper())
    logging.root.setLevel(log_level)

    # Clear existing handlers
    logging.root.handlers.clear()

    # Add stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    logging.root.addHandler(stdout_handler)

    # Add file handler with rotation (if enabled)
    if settings.LOG_FILE_ENABLED:
        # Create logs directory if it doesn't exist
        log_dir = Path(settings.LOG_FILE_PATH)
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{settings.OTEL_SERVICE_NAME}.log"
        file_handler = TimedRotatingFileHandler(
            filename=str(log_file),
            when="D",  # Daily rotation
            interval=1,
            backupCount=settings.LOG_FILE_RETENTION_DAYS,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        logging.root.addHandler(file_handler)

    # Configure structlog processors based on environment
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.ENVIRONMENT == "development":
        # Clean console output for development
        # Disable colors by default since Docker logs don't render ANSI codes properly
        # Users can enable colors by setting ENABLE_LOG_COLORS=true if running in a proper terminal
        processors.append(
            structlog.dev.ConsoleRenderer(
                colors=settings.ENABLE_LOG_COLORS,
                sort_keys=False,
                exception_formatter=structlog.dev.plain_traceback,
            )
        )
    else:
        # JSON output for production
        processors.append(structlog.processors.JSONRenderer())

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def setup_otel(settings: BaseAppSettings) -> None:
    """Initialize OpenTelemetry with OTLP exporter.

    Args:
        settings: Application settings with OTEL configuration

    """
    if not settings.OTEL_ENABLED:
        return

    # Set up resource attributes
    resource = Resource.create(
        {
            "service.name": settings.OTEL_SERVICE_NAME,
            "deployment.environment": settings.ENVIRONMENT,
        }
    )

    # Configure trace provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Configure OTLP exporter with Honeycomb headers if API key provided
    headers = {}
    if settings.HONEYCOMB_API_KEY:
        headers["x-honeycomb-team"] = settings.HONEYCOMB_API_KEY

    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{settings.OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces",
        headers=headers,
    )

    # Add span processor
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Instrument logging to inject trace context
    LoggingInstrumentor().instrument(set_logging_format=False)


def setup_sentry(settings: BaseAppSettings) -> None:
    """Initialize Sentry with OTEL integration.

    Args:
        settings: Application settings with Sentry configuration

    Note:
        Use `extra={"sentry_fingerprint": ["error-type"]}` in logger calls
        to prevent duplicate issues per user in Sentry.

    Example:
        logger.error(
            "llm_processing_failed",
            error_type="timeout",
            extra={"sentry_fingerprint": ["llm-timeout"]}
        )

    """
    if not settings.SENTRY_DSN:
        return

    # Configure Sentry SDK
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        # Enable performance monitoring
        traces_sample_rate=1.0 if settings.ENVIRONMENT == "development" else 0.1,
        # Enable profiling
        profiles_sample_rate=1.0 if settings.ENVIRONMENT == "development" else 0.1,
        # Capture logs
        integrations=[
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above
                event_level=logging.ERROR,  # Only send errors to Sentry
            ),
        ],
        # Before send hook for custom fingerprinting
        before_send=_sentry_before_send,  # type: ignore[arg-type]
    )


def _sentry_before_send(event: dict[str, Any], hint: dict[str, Any]) -> dict[str, Any] | None:
    """Process events before sending to Sentry.

    Extracts fingerprint from log record's extra dict if present.

    Args:
        event: Sentry event dict
        hint: Additional context

    Returns:
        Modified event or None to drop event

    """
    if "log_record" in hint:
        record = hint["log_record"]
        if hasattr(record, "sentry_fingerprint"):
            event["fingerprint"] = record.sentry_fingerprint

    return event


def setup_observability(settings: BaseAppSettings) -> None:
    """Master function to set up all observability components.

    Args:
        settings: Application settings with observability configuration

    """
    setup_logging(settings)
    setup_otel(settings)
    setup_sentry(settings)

    logger = structlog.get_logger(__name__)
    logger.info(
        "observability_initialized",
        environment=settings.ENVIRONMENT,
        log_level=settings.LOG_LEVEL,
        otel_enabled=settings.OTEL_ENABLED,
        sentry_enabled=bool(settings.SENTRY_DSN),
    )
