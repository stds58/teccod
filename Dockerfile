FROM python:3.13-slim AS builder

ARG WORKDIR=/opt/backend

WORKDIR $WORKDIR
RUN pip install uv
ENV PATH="$WORKDIR/.venv/bin:$PATH"

COPY pyproject.toml .
RUN uv sync;


FROM python:3.11-slim

ARG WORKDIR=/opt/backend
ARG USER=appuser

WORKDIR $WORKDIR
COPY --from=builder $WORKDIR/.venv $WORKDIR/.venv
ENV PATH="$WORKDIR/.venv/bin:$PATH"
RUN useradd -m appuser

COPY . .

ENV PATH="$WORKDIR/.venv/bin:$PATH"
USER appuser

CMD ["python", "app.py"]
