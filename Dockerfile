FROM python:3.12-slim

# Install curl for downloading uv
RUN apt-get update && apt-get install -y curl ca-certificates && \
    curl -Ls https://astral.sh/uv/install.sh | sh && \
    apt-get purge -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install dependencies (except project itself)
COPY uv.lock pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

COPY flibusta_bot flibusta_bot/
COPY README.md README.md
COPY logs logs/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

EXPOSE 9998

# Run the application
CMD  uv run -m flibusta_bot
