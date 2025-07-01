ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /techagro

WORKDIR /techagro

RUN pip install poetry
COPY pyproject.toml poetry.lock /techagro/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY ./techagro /techagro

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","1","config.wsgi"]
