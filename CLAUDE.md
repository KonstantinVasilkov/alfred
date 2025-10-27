# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Alfred is a Python 3.13+ monorepo project using UV workspace management. The project consists of multiple apps and shared libraries:

**Apps:**
- `apps/telegram_bot` - Telegram bot with LLM integration (Anthropic Claude via pydantic-ai)
- `apps/finances_api` - Finances API (planned)
- `apps/llm_connectors` - LLM connectors (planned)

**Libs:**
- `libs/llm` - LLM abstractions (LLMAgent interface) and implementations (AnthropicAgent)
- `libs/shared_infra` - Infrastructure utilities (config base, logging)
- `libs/shared_domain` - Shared domain models

## Configuration

Each app has its own configuration module using Pydantic Settings, inheriting from `BaseAppSettings` in `libs/shared_infra`:
- Create a `.env` file in the project root for local development
- App settings use `env_prefix` for namespacing (e.g., `TELEGRAM__BOT_TOKEN`)
- Common settings (LOG_LEVEL, SENTRY_DSN) are defined in `BaseAppSettings`
- Use `get_settings()` in each app to access configuration

## Development Workflow

This project follows **Trunk-Based Development** (see trunkbaseddevelopment.com):
- Work on short-lived feature branches (max 1-2 days)
- Merge frequently to `main` branch
- Keep `main` always releasable
- Use feature flags for incomplete features if needed

### Git Workflow
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make changes and commit frequently
3. Run pre-commit hooks before pushing: `make pre-commit`
4. Push and create a pull request to `main`
5. After merge, delete the feature branch

### Commit Message Convention
Follow the Conventional Commits specification:

**Format:**
```
type: imperative summary (<50 chars)

Optional body providing context in 1-2 sentences.
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Rules:**
- Start with imperative verb (e.g., "add", "fix", "update")
- Keep summary under 50 characters
- Leave empty line before body
- No special symbols before or after commit text
- Body should explain motivation and impact (1-2 sentences)
- Never mention Anthropic or Claude in commit messages
- Never use emojis in commit messages

### Pre-commit Hooks
Pre-commit hooks run automatically before each commit:
- **ruff**: Linting and formatting
- **pyright**: Type checking

Install hooks: `make pre-commit-install`
Run manually: `make pre-commit`

## Development Commands

### Makefile shortcuts
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

### Running the application

**Telegram Bot (Local):**
```bash
make run-app APP=telegram_bot
```

**Docker:**
```bash
make docker-up
```

View logs:
```bash
docker compose -f deploy/docker-compose.dev.yml logs -f telegram_bot
```

**Per-app commands:**
```bash
make test-app APP=telegram_bot      # Run tests for specific app
make lint-app APP=telegram_bot      # Lint specific app
make typecheck-app APP=telegram_bot # Type check specific app
```

### Dependency management
This project uses `uv` for dependency management:
```bash
uv add <package>        # Add production dependency
uv add --dev <package>  # Add development dependency
uv sync                 # Install all dependencies
```

## Code Style

### Naming Conventions
- **Files/directories**: `snake_case` (e.g., `company_service.py`)
- **Classes**: `PascalCase` (e.g., `CompanyService`)
- **Functions/variables**: `snake_case` (e.g., `get_company_by_id`)
- **Function calls**: Always use explicit parameter names

### Type Safety
- Use type hints for all function signatures
- Prefer modern Python union syntax: `dict[str, Any] | None` over `Optional[dict[str, Any]]`
- Use Pydantic models over raw dictionaries for input validation
- Run `make typecheck` to check types across all apps and libs
- Type checking is done with **pyright** in strict mode (configured in `pyrightconfig.json`)
- The monorepo structure is handled via execution environments in pyright config
- Add `# pyright: ignore[errorCode]` comments sparingly for legitimate false positives

### Import Organization
- **All imports must be at the top of the file** - no exceptions
- Never use inline imports or lazy imports as workarounds
- Circular imports indicate architectural problems - fix the architecture, not the imports
- Only use inline imports as an absolute last resort when no other solution exists
- If circular imports occur, refactor to break dependencies (extract interfaces, use dependency inversion, restructure modules)

## Testing

- Every development stage must end with tests
- **NEVER modify existing tests without explicit user consent**
- Target coverage: 85-90%
- Focus on integration tests and e2e tests; minimize unit tests
- Tests validate the system's behavior as a whole rather than isolated components

## Architecture

This project follows principles from "Architecture Patterns with Python" by Harry Percival and Bob Gregory:

- **Domain Model**: Business logic expressed in pure Python objects, free from infrastructure concerns
- **Repository Pattern**: Abstract data access behind repository interfaces
- **Service Layer**: Orchestrate use cases, coordinate between domain model and repositories
- **Unit of Work Pattern**: Manage atomic operations and transactions
- **Dependency Inversion**: High-level modules don't depend on low-level modules; both depend on abstractions

### Project Structure
The project follows a monorepo structure with UV workspace:
- **apps/** - Independent application packages (telegram_bot, finances_api, llm_connectors)
- **libs/** - Shared libraries used across apps (llm, shared_infra, shared_domain)

Within each app/lib, follow this layered architecture:
- **Domain layer**: Core business logic and entities
- **Service layer**: Application use cases and orchestration
- **Adapters layer**: External integrations (repositories, APIs, etc.)
- **Entrypoints**: Bot handlers, API endpoints, CLI commands

Each app has its own entry point in `apps/<app_name>/<app_name>/main.py:main()`.

### Docker Configuration
- Docker compose is configured for development in `deploy/docker-compose.dev.yml`
- Dockerfiles are located in each app directory
- Build context is set to monorepo root to access all workspace members
- Environment variables use app-specific prefixes (e.g., `TELEGRAM__` for telegram_bot)
- Apps run as non-root user (alfred:999) for security


## Context7
## Use Context7 by Default
Always use context7 when I need code generation, setup or configuration steps, or library/API documentation. This means you should automatically use the Context7 MCP tools to resolve library id and get library docs without me having to explicitly ask.


[[calls]]
match = "when the user requests code examples, setup or configuration steps, or library/API documentation"
tool  = "context7"