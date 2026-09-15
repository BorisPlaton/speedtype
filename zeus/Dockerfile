FROM python:3.14 AS base

COPY uv.lock pyproject.toml ./
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/
RUN uv venv -p 3.14 && \
    . .venv/bin/activate && \
    uv sync --frozen

FROM python:3.14-slim AS backend-app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src"
ENV PATH="/app/.venv:${PATH}"

RUN useradd -ms /bin/sh -u 1001 app
COPY --from=base --chown=app:app /.venv /app/.venv
COPY --chown=app:app . ./

USER app

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
    CMD curl "localhost:${ZEUS_PORT}/health"

ENTRYPOINT ["python", "./src/inbound/http"]
