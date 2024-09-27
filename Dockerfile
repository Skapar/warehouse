FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y make

RUN pip install --upgrade pip \
    && pip install poetry

RUN poetry config virtualenvs.create false

# Install the dependencies
RUN poetry install --no-dev

COPY ./warehouse-application ./warehouse-application

WORKDIR /app/warehouse-application

EXPOSE 8000

CMD ["python", "main.py"]