# Builder stage
FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Runtime stage
FROM python:3.13-slim

# Create non-root user
RUN useradd -m -u 1000 alfred && \
    mkdir -p /app && \
    chown -R alfred:alfred /app

WORKDIR /app

# Copy uv from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=alfred:alfred alfred/ ./alfred/
COPY --chown=alfred:alfred main.py ./

# Switch to non-root user
USER alfred

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/app/.venv"

# Run the application
CMD ["/app/.venv/bin/python", "main.py"]
