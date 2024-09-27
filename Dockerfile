FROM python:3.12.6

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

RUN warehouse-application/alembic revision --autogenerate -m 'initial'

RUN warehouse-application/alembic upgrade head

COPY . .

EXPOSE 8000

CMD ["python", "warehouse-application/main.py"]
