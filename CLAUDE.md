# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Alfred is a Python 3.13+ project in early development stage. Currently contains minimal scaffolding with a single entry point in `main.py`.

## Configuration

Project settings are managed using Pydantic Settings (`alfred/config.py`) and loaded from environment variables/.env files:
- Create a `.env` file in the project root for local development
- All settings are defined in the `Settings` class
- Use `get_settings()` to access configuration throughout the application

## Development Commands

### Running the application
```bash
python main.py
```

### Dependency management
This project uses `uv` for dependency management:
```bash
uv add <package>        # Add production dependency
uv add --dev <package>  # Add development dependency
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
