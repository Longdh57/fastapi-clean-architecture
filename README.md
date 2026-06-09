# Book Management API — FastAPI + Clean Architecture

A simple book-management REST API demonstrating **Clean Architecture** with
FastAPI, SQLite, SQLAlchemy, Alembic migrations and Pydantic schemas.

## Architecture

Dependencies point **inward** — outer layers depend on inner layers, never the
reverse. The domain knows nothing about FastAPI or SQLAlchemy.

```
app/
├── domain/                  # Enterprise rules — pure Python, no frameworks
│   ├── entities/book.py             # Book entity + invariants
│   └── repositories/book_repository.py   # Repository interface (port)
│
├── application/             # Application rules — orchestrates the domain
│   ├── use_cases/book_use_cases.py  # Create / read / update / delete logic
│   └── exceptions.py                # Domain-level errors
│
├── infrastructure/         # Frameworks & drivers (adapters)
│   ├── database/connection.py       # Engine + session factory
│   ├── database/models.py           # SQLAlchemy ORM model
│   └── repositories/book_repository_impl.py  # Repository implementation
│
├── presentation/           # Interface adapters — HTTP layer
│   ├── api/v1/books.py              # FastAPI routes
│   ├── schemas/book.py             # Pydantic request/response models
│   └── dependencies.py             # Dependency injection wiring
│
├── config.py               # Pydantic settings
└── main.py                 # FastAPI app entry point
```

The flow of a request: **route → use case → repository interface →
repository implementation → database**. The use case depends only on the
abstract `BookRepository`; the concrete SQLAlchemy adapter is injected at the
edge in `dependencies.py`, so the business logic stays testable and
DB-agnostic.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optionally copy the env template (defaults work out of the box):

```bash
cp .env.example .env
```

## Database migrations (Alembic)

```bash
# Apply migrations — creates books.db with the books table
alembic upgrade head

# After changing models.py, autogenerate a new migration
alembic revision --autogenerate -m "describe your change"

# Roll back the most recent migration
alembic downgrade -1
```

## Run the server

```bash
uvicorn app.main:app --reload
```

- API base: <http://127.0.0.1:8000/api/v1>
- Interactive docs (Swagger UI): <http://127.0.0.1:8000/docs>
- Alternative docs (ReDoc): <http://127.0.0.1:8000/redoc>

## API endpoints

| Method | Path                  | Description            |
|--------|-----------------------|------------------------|
| GET    | `/`                   | Health check           |
| POST   | `/api/v1/books`       | Create a book          |
| GET    | `/api/v1/books`       | List books (paginated) |
| GET    | `/api/v1/books/{id}`  | Get a book by id       |
| PUT    | `/api/v1/books/{id}`  | Update a book          |
| DELETE | `/api/v1/books/{id}`  | Delete a book          |

### Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/books \
  -H 'Content-Type: application/json' \
  -d '{
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "isbn": "9780134494166",
        "published_year": 2017,
        "description": "A craftsman'\''s guide to software structure."
      }'
```

Duplicate ISBNs return `409 Conflict`; unknown ids return `404 Not Found`.
