FROM python:3.12.0

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install 'poetry==1.6.1'
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi --no-dev

COPY . .

CMD chmod a+x scripts/*sh &&  \
    /app/scripts/run_migration.sh

WORKDIR /app/src
