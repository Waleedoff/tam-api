# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the API (with hot reload):**
```bash
docker compose up api --build
```
API is available at `http://localhost:3002`. Swagger UI at `/docs`.

**Run all tests:**
```bash
docker compose run tam-pytest
```

**Run a single test file:**
```bash
docker compose run tam-pytest pytest testing/src/todos/test_todo_user_data.py
```

**Lint and format:**
```bash
ruff check .
ruff format .
```

**Type check:**
```bash
mypy .
```

**Database migrations:**
```bash
# Apply migrations
alembic upgrade head

# Generate a new migration
alembic revision --autogenerate -m "description"
```

## Architecture

This is a FastAPI backend for an agile project management tool (TAM). It uses PostgreSQL (via SQLAlchemy), Redis (caching + Celery broker), and Celery for async tasks.

### Module structure

Each API feature under `app/api/<module>/` follows this layout:
- `routes.py` — FastAPI router; exports `router`, `prefix`, and `tags`
- `models.py` — SQLAlchemy ORM models
- `schema.py` — Pydantic request/response schemas
- `enums.py` — module-specific enums
- `services/` or `service/` — one file per operation (e.g. `create_task.py`, `get_tasks.py`)

All routers are registered in `app/main.py` by iterating a `routes` list.

### Base model (`app/db/db.py`)

All models inherit from `Base` and `Defaults`. `Defaults` automatically:
- Generates `__tablename__` from the class name (CamelCase → snake_case + `s`), overridable via `__override_tablename__`
- Adds `id` (UUID string, primary key), `created_by`, `created`, `updated`
- Provides `update_attributes(dict)` to patch model fields, with support for nullifying fields via `columns_to_deleted`

### Dependency injection (`app/dependencies.py`)

Pre-built FastAPI `Depends` instances for use directly in route signatures:
- `db_session` — write DB session (wraps `SessionLocal`)
- `db_read_session` — read-only DB session (wraps `ReadSessionLocal`)
- `redis_client` — Redis client
- `role_required(*roles)` — JWT-based role guard

Auth for endpoints: use `Depends(get_current_active_user)` from `app/api/auth/services/authSetup.py`.

### Configuration (`app/config.py`)

`BaseConfig` (Pydantic Settings) loads from environment / `.env`. Config variant is selected by the `ENVIRONMENT` env var: `local` → `BaseConfig`, `staging` → `StagingConfig`, `testing` → `TestingConfig`, `prod` → `ProductionConfig`. In production, `openapi_url` is set to `None` (disables Swagger).

### Testing (`testing/`)

`conftest.py` wraps each test in a nested SQLAlchemy transaction that rolls back after the test — no data persists between tests. The `tam-pytest` Docker service creates and drops a separate `tam_testing` database. The `client` fixture is `scope="session"` and overrides `get_db_session` / `get_db_read_session` with the transactional session.

### LangChain / AI (`core/langChain/`)

An AI layer for natural-language SQL queries and automatic task breakdown from user stories. Routes are under `/agent`. Uses `OPENAI_API_KEY` from config. Task assignment uses round-robin by department from room members.

### Background tasks (`app/celery_worker/`)

Celery app initialized in `app.py`, tasks registered in `tasks.py`. Currently handles email sending (`send_email_task`). The broker is Redis. In tests, Celery tasks are overridden to use the scoped test session.

### Domain model summary

- **Room** — a project workspace; has a product owner, members (`RoomMember`), and user stories
- **Sprint** — belongs to a room; groups user stories across a time period
- **UserStory** — belongs to a sprint; has actor, acceptance criteria, priority
- **Todo** (task) — belongs to a user story, sprint, and room; assigned to a user
- **Backlog** — unscheduled items linked to a room
- **Goal** / **KeyResult** — OKR-style objectives with deadlines
- **Announcement** — room-level announcements with votes and comments
- **Organization** — top-level tenant; users and rooms belong to an org
