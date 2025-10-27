# Alfred

A Telegram bot built with Python 3.13+ and aiogram, following clean architecture principles.

## Features

- Telegram bot with LLM integration (Anthropic Claude via pydantic-ai)
- Monorepo structure with UV workspace management
- Pydantic Settings for configuration management
- Docker containerization with UV workspace support
- Pre-commit hooks for code quality (ruff, pyright)
- Trunk-based development workflow
- GitHub Actions CI with path-based filtering
- **Comprehensive observability** with structlog, OpenTelemetry, and Sentry

## Observability

Alfred includes a production-ready observability stack:

### Stack
- **Structured logging** with [structlog](https://www.structlog.org/) - Context-rich logs, JSON output in production
- **OpenTelemetry** - Vendor-neutral telemetry export to Honeycomb, Grafana, Jaeger, etc.
- **Sentry** - Error tracking with automatic fingerprinting to prevent duplicate issues
- **Log files** - 7-day rotation with configurable retention

### Quick Start

**Development** (pretty console logs):
```bash
# Default configuration in .env
TELEGRAM__ENVIRONMENT=development
TELEGRAM__LOG_LEVEL=INFO
TELEGRAM__OTEL_ENABLED=false
```

**Production** (JSON logs + OTEL + Sentry):
```bash
# Enable full observability
TELEGRAM__ENVIRONMENT=production
TELEGRAM__OTEL_ENABLED=true
TELEGRAM__OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io
TELEGRAM__HONEYCOMB_API_KEY=your_api_key
TELEGRAM__SENTRY_DSN=your_sentry_dsn
```

### Free Tier Options

| Service | Free Tier | What to Track |
|---------|-----------|---------------|
| [Honeycomb](https://honeycomb.io) | 20M events/month | Logs, traces, performance |
| [Sentry](https://sentry.io) | 5K errors/month | Exceptions, error rates |
| [Grafana Cloud](https://grafana.com/products/cloud/) | 50GB logs | Alternative to Honeycomb |

### Key Features

**Context Binding** - Automatically include fields in all logs:
```python
from shared_infra import bind_context, get_logger

logger = get_logger(__name__)
bind_context(user_id=123, chat_id=456)  # Added to all subsequent logs
logger.info("message_received")  # Includes user_id and chat_id
```

**Sentry Fingerprinting** - Group errors to avoid quota exhaustion:
```python
logger.exception(
    "llm_timeout",
    extra={"sentry_fingerprint": ["llm-timeout"]}  # All LLM timeouts = 1 issue
)
```

**Timing** - Automatic performance tracking:
```python
start = time.time()
result = await process()
logger.info("completed", duration_seconds=time.time() - start)
```

See [CLAUDE.md](CLAUDE.md#observability) for detailed usage patterns and configuration.

## Prerequisites

- Python 3.13+
- Docker and Docker Compose (for containerized deployment)
- uv (for dependency management)
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd alfred
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials (use `TELEGRAM__` prefix):

```
TELEGRAM__BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM__ANTHROPIC_API_KEY=your_anthropic_api_key_here
TELEGRAM__LLM_MODEL=claude-3-5-sonnet-latest
```

### 3. Install dependencies (for local development)

```bash
make install
```

Or manually:

```bash
uv sync
```

### 4. Install pre-commit hooks (optional, for development)

```bash
make pre-commit-install
```

## Running the Bot

### Using Docker (Recommended)

Start the bot:

```bash
make docker-up
```

View logs:

```bash
docker compose -f deploy/docker-compose.dev.yml logs -f telegram_bot
```

Stop the bot:

```bash
make docker-down
```

### Local Development

```bash
make run-app APP=telegram_bot
```

Or directly:

```bash
cd apps/telegram_bot && uv run python -m telegram_bot.main
```

## Development

### Available Make Commands

```bash
make install          # Install dependencies
make test             # Run tests
make lint             # Run ruff linting
make format           # Format code with ruff
make typecheck        # Run pyright type checking
make pre-commit       # Run all pre-commit hooks
make docker-up        # Start services with docker-compose
make docker-down      # Stop docker-compose services
make clean            # Clean cache files
```

### Running Tests

```bash
make test
```

Or with pytest directly:

```bash
uv run pytest tests/ -v
```

### Code Quality

Run all checks before committing:

```bash
make pre-commit
```

Or run individual checks:

```bash
make lint        # Check code style
make format      # Auto-format code
make typecheck   # Type checking with pyright
```

## Architecture

This project follows principles from "Architecture Patterns with Python":

- **Domain Model**: Business logic in pure Python objects
- **Repository Pattern**: Abstract data access
- **Service Layer**: Orchestrate use cases
- **Dependency Inversion**: Depend on abstractions

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## Project Structure

```
alfred/                      # UV workspace monorepo
├── apps/                    # Application packages
│   ├── telegram_bot/        # Telegram bot with LLM integration
│   ├── finances_api/        # Finances API (planned)
│   └── llm_connectors/      # LLM connectors (planned)
├── libs/                    # Shared libraries
│   ├── llm/                 # LLM abstractions and implementations
│   ├── shared_infra/        # Infrastructure utilities (config, logging)
│   └── shared_domain/       # Shared domain models
├── deploy/                  # Docker and deployment configs
│   └── docker-compose.dev.yml
├── .github/                 # GitHub Actions CI/CD
├── pyproject.toml           # Workspace configuration
├── pyrightconfig.json       # Type checking configuration
├── Makefile                 # Development shortcuts
├── CLAUDE.md                # Development guidelines
└── .env.example             # Environment variables template
```

## License

[Add your license here]
