FROM python:3.10-slim

ENV PYTHONBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install pipenv

RUN pipenv install --system --deploy --clear --ignore-pipfile

ENTRYPOINT ["/app/docker_entrypoint.sh"]