# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Alfred is a Python 3.13+ project in early development stage. Currently contains minimal scaffolding with a single entry point in `main.py`.

## Configuration

Project settings are managed using Pydantic Settings (`alfred/config.py`) and loaded from environment variables/.env files:
- Create a `.env` file in the project root for local development
- All settings are defined in the `Settings` class
- Use `get_settings()` to access configuration throughout the application

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
- **mypy**: Type checking

Install hooks: `make pre-commit-install`
Run manually: `make pre-commit`

## Development Commands

### Makefile shortcuts
```bash
make install          # Install dependencies
make test             # Run tests
make lint             # Run ruff linting
make format           # Format code with ruff
make typecheck        # Run mypy type checking
make pre-commit       # Run all pre-commit hooks
make docker-build     # Build Docker image
make docker-up        # Start services with docker-compose
make docker-down      # Stop docker-compose services
make clean            # Clean cache files
```

### Running the application

**Local:**
```bash
python main.py
```

**Docker:**
```bash
make docker-up
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
The project is currently in its initial setup phase. As it grows, follow this layered architecture:
- **Domain layer**: Core business logic and entities
- **Service layer**: Application use cases and orchestration
- **Adapters layer**: External integrations (repositories, APIs, etc.)
- **Entrypoints**: Web controllers, CLI commands, etc.

The main entry point is `main.py:main()`.


## Context7
## Use Context7 by Default
Always use context7 when I need code generation, setup or configuration steps, or library/API documentation. This means you should automatically use the Context7 MCP tools to resolve library id and get library docs without me having to explicitly ask.


[[calls]]
match = "when the user requests code examples, setup or configuration steps, or library/API documentation"
tool  = "context7"