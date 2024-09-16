FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && \
    poetry install --no-interaction --no-ansi

COPY . /app

RUN poetry run pytest

RUN poetry run alembic upgrade head

ENTRYPOINT ["poetry", "run", "python", "main.py"]
CMD ["input.txt"]
