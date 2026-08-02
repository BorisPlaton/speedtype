FROM python:3.14 AS base

COPY uv.lock pyproject.toml .
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/
RUN uv venv -p 3.14 && \
    . .venv/bin/activate && \
    uv sync --frozen

FROM python:3.14-slim AS backend-app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src"
ENV PATH="/.venv/bin:${PATH}"

RUN useradd -ms /bin/sh -u 1001 app
COPY --from=base /.venv /.venv
COPY --chown=app:app . .

ENTRYPOINT ["python", "./src/inbound/http"]
