# Warehouse Application

## Overview

The Warehouse application is built using FastAPI, SQLAlchemy, and PostgreSQL. It provides an API for managing orders and products in a warehouse.

## Project Structure

```structure
warehouse-application/
├── alembic/
│   └── versions/
├── core/
├── crud/
├── logs/
│   └── app.log
├── utils/
├── main.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy (asyncio)
- Asyncpg
- Alembic

## Setup

1. **Create a `.env` file** in the `warehouse-application` folder with the following content:

    ```plaintext
    APP_CONFIG__DB__URL=postgresql+asyncpg://postgres:123@db:5432/warehouse
    APP_CONFIG__DB__ECHO=1

    DATABASE_URL=postgresql+asyncpg://postgres:123@db:5432/warehouse
    ```

2. **Install dependencies** using Poetry:

    ```bash
    poetry install
    ```

## Running the Application

You can build and run the application using the Makefile:

1. **Build the application**:

    ```bash
    make build
    ```

2. **Run the application**:

    ```bash
    make run
    ```

## API Endpoints

- **POST /api/v1/orders**: Create a new order.
- **GET /api/v1/products**: Retrieve a list of products.
- **GET /api/v1/orders/{order_id}**: Retrieve details of a specific order.

## Logging

Logs are saved in the `logs/app.log` file.

## Database Migrations

Migrations are managed using Alembic. To create a new migration, run:

```bash
alembic revision --autogenerate -m "Migration message"
```

To apply migrations, run:

```bash
alembic upgrade head
```

## Future Enhancements

I intended to implement role-based access control to enhance security and user management but didn't have enough time to complete this feature. I am so sorry for this :(

## License

This project is licensed under the MIT License.
