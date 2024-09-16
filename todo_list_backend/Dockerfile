FROM python:3.12.0

WORKDIR /todo_list_backend/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install 'poetry==1.6.1'
COPY poetry.lock pyproject.toml /todo_list_backend/

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi --no-dev

COPY . .

CMD chmod a+x scripts/*sh &&  \
    /todo_list_backend/scripts/run_migration.sh

WORKDIR /todo_list_backend/src
