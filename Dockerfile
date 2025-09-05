FROM python:3.13-slim AS builder

ARG WORKDIR=/opt/backend
WORKDIR $WORKDIR

RUN pip install uv
ENV PATH="$WORKDIR/.venv/bin:$PATH"

COPY pyproject.toml .
RUN uv sync;


FROM python:3.13-slim

ARG WORKDIR=/opt/backend
ARG USER=appuser
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

COPY --from=builder $WORKDIR/.venv $WORKDIR/.venv
ENV PATH="$WORKDIR/.venv/bin:$PATH"
ENV PYTHONPATH="${WORKDIR}"
RUN useradd -m $USER
USER $USER

COPY . .

ENV PATH="$WORKDIR/.venv/bin:$PATH"
USER appuser


ENTRYPOINT ["./init.sh"]
#CMD ["python", "app/utils/init_opensearch.py"]
#CMD ["sleep", "infinity"]
#CMD ["uvicorn app.main:app --workers 4 --host 0.0.0.0"]
CMD ["uvicorn", "app.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]