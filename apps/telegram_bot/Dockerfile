# Use Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Setup non-root user
RUN groupadd --system --gid 999 alfred \
 && useradd --system --gid 999 --uid 999 --create-home alfred

WORKDIR /app

# Configure uv environment
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy workspace configuration and lockfile
COPY pyproject.toml uv.lock ./

# Copy all workspace members (needed for dependency resolution)
COPY libs ./libs
COPY apps/telegram_bot ./apps/telegram_bot
COPY apps/finances_api/pyproject.toml ./apps/finances_api/
COPY apps/llm_connectors/pyproject.toml ./apps/llm_connectors/

# Install dependencies from workspace root
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package telegram-bot

# Configure path and switch to non-root user
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/apps/telegram_bot
USER alfred

# Run the application
CMD ["python", "-m", "telegram_bot.main"]
