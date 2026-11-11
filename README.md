# FastAPI-SaaS-Boilerplate (`fastapi-saas-boilerplate`)

> A structured boilerplate for building multi-tenant SaaS backends with FastAPI using a modular monolith pattern and Domain-Driven Design (DDD).

---

## Architecture Overview

This template organizes code by business capabilities rather than technical roles:

- **`domains/`:** Bounded contexts (`tenancy`, `users`, `billing`) isolate business logic.
- **`core/`:** Technical plumbing like the database engine, security, and middleware.
- **`common/`:** Shared utilities and primitives used across domains.
- **Cross-Domain Workflows:** Handled via service-layer transactions (for example, creating a user and their initial tenant during registration).

---

## Directory Structure

```text
server/
├── alembic/                    # Database migrations
├── core/                       # Infrastructure plumbing (DB, security, lifespan)
├── common/                     # Shared utilities (pagination, slugify)
├── domains/                    # Bounded contexts
│   ├── tenancy/                # Organizations and workspace management
│   ├── billing/                # Subscriptions and usage meters
│   └── users/                  # User accounts, authentication, and profiles
│       ├── models.py           # SQLAlchemy User model
│       ├── schemas.py          # Pydantic request/response models
│       ├── services.py         # Business logic and registration workflow
│       ├── router.py           # Auth endpoints
│       └── security.py         # Password hashing and token utilities
├── scripts/                    # Operational scripts (seeding, openapi export)
├── tests/                      # Domain-mapped unit and integration tests
├── .env                        # Local environment variables
├── .env.example                # Environment variables template
├── Dockerfile                  # Container definition
├── config.py                   # Root-level Pydantic settings
├── main.py                     # FastAPI application factory
├── pyproject.toml              # Dependencies and project metadata
└── uv.lock                     # Dependency lock file
```
