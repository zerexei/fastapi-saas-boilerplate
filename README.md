# FastAPI-SaaS-Boilerplate

A modular starter template for building full-stack applications with FastAPI, SQLAlchemy (Async), PostgreSQL, Redis, and a Vite React frontend. It separates core infrastructure from business logic and uses explicit dependency injection for database sessions and caching.

---

## What's Included

- **FastAPI Backend:** Configured with an application factory pattern, custom exception handling, structured logging, and lifespan event management.
- **Domain-Driven Layout:** Business logic is organized into isolated domains (`domains/users/`) with dedicated models, schemas, routers, and services.
- **Database & Cache Management:** SQLAlchemy 2.0 with async support, Alembic migrations, and separate read (`SessionDep`) and transaction (`TxSessionDep`) session dependencies.
- **Frontend Integration:** Vite React setup with automated OpenAPI type generation from the backend spec.
- **Developer Tooling:** Unified task runner via `Makefile` and local services managed through Docker Compose.

---

## Project Directory Layout

```text
├── client/                 # Vite React frontend application
├── server/                 # FastAPI backend application
│   ├── alembic/            # Database migration scripts
│   ├── common/             # Shared utilities (base models, string helpers)
│   ├── core/               # Configuration, database, cache, security, and middleware
│   ├── domains/            # Feature modules (e.g., users)
│   ├── scripts/            # CLI utilities (seeders, openapi export)
│   ├── tests/              # Pytest test suite
│   └── main.py             # Application factory entrypoint
├── infra/                  # Docker Compose configurations (PostgreSQL, Redis)
└── Makefile                # Developer task runner
```

---

## Getting Started

### 1. Prerequisites

- Python 3.12+ and `uv`
- Node.js and `pnpm`
- Docker and Docker Compose

### 2. Environment Configuration

Copy the sample environment files and update them with your local credentials:

```bash
cp server/.env.example server/.env
cp client/.env.example client/.env
```

### 3. Start Infrastructure

Run Docker Compose to spin up PostgreSQL and Redis:

```bash
make up
```

### 4. Run Database Migrations

Apply the initial database schema:

```bash
make migrate
```

### 5. Run Development Servers

Start the backend and frontend servers in separate terminal tabs:

```bash
# Terminal 1: Backend
make server-dev

# Terminal 2: Frontend
make client-dev
```

- Backend API Docs: `http://localhost:8000/docs`
- Frontend App: `http://localhost:5173`

---

## How to Add a New Domain

To add a new feature domain (for example, `subscriptions`), create a new folder under `server/domains/` with the following structure:

```text
server/domains/subscriptions/
├── models.py      # SQLAlchemy database models
├── schemas.py     # Pydantic request/response validation
├── service.py     # Business logic class receiving cache/dependencies
├── dependencies.py# Domain-specific FastAPI dependencies
└── router.py      # APIRouter endpoints
```

Then, register the router in `server/main.py` inside the `_register_routes` function:

```python
app.include_router(subscriptions_router, prefix="/api/v1", tags=["subscriptions"])
```

---

## Makefile Reference

- **`make up`** — Start local database and Redis containers.
- **`make down`** — Stop infrastructure containers.
- **`make logs`** — View container logs.
- **`make migrate`** — Apply pending database migrations.
- **`make migration-create msg="..."`** — Generate a new migration file.
- **`make server-dev`** — Run the FastAPI backend development server.
- **`make client-dev`** — Run the Vite React frontend development server.
- **`make test-server`** — Run backend tests with pytest.
- **`make test-client`** — Run frontend tests.
- **`make types`** — Export OpenAPI spec and generate TypeScript definitions for the client.

---

## License

Distributed under the MIT License.
