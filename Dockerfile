# Use Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Setup non-root user
RUN groupadd --system --gid 999 alfred \
 && useradd --system --gid 999 --uid 999 --create-home alfred

WORKDIR /app

# Configure uv environment
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies using uv with cache mount
RUN --mount=type=cache,target=/root/.cache/uv \
 --mount=type=bind,source=uv.lock,target=uv.lock \
 --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
 uv sync --frozen --no-install-project --no-dev

# Copy project and install
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
 uv sync --frozen --no-dev

# Configure path and switch to non-root user
ENV PATH="/app/.venv/bin:$PATH"
USER alfred

# Run the application
CMD ["python", "main.py"]
