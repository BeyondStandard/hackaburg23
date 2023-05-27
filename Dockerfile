FROM python:3.9-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PATH=/opt/pipx/bin:/app/.venv/bin:$PATH \
    PIPX_BIN_DIR=/opt/pipbx/bin \
    PIPX_HOME=/opt/pipx/home \
    POETRY_VERSION=1.5.0

RUN pip install --no-cache-dir --upgrade pip pipx
RUN pipx ensurepath
RUN pipx install "poetry==$POETRY_VERSION"

FROM base AS deps
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --without test,dev --no-interaction --no-ansi

FROM deps AS development
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only test,dev --no-interaction --no-ansi
COPY . .

FROM deps AS build
WORKDIR /app
COPY . .
RUN poetry build

FROM base AS production
WORKDIR /app
COPY --from=build /app/dist ./
RUN pipx install *.tar.gz
CMD ["python", "hackaburg23_frontend/app.py"]