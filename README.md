# Best-Shorter

> A blazing-fast, production-ready URL shortener — built on Python 3.13, FastAPI, and PostgreSQL.

[![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![uv](https://img.shields.io/badge/uv-package_manager-DE5FE9?logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/linted_by-Ruff-FCC21B?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)

---

## What Is It?

Best-Shorter turns long, unwieldy URLs into clean short links — and tracks everything that happens after the click.

Every visit is captured: location, device, browser, referrer, and uniqueness. Counters stay consistent at the database level. Links can expire, be owned by a user, or be completely anonymous.

The service speaks ASGI, runs on [Granian](https://github.com/emmett-framework/granian) (a Rust-powered HTTP server), and is ready to deploy behind any reverse proxy.

---

## Features

- **Short link generation** with unique codes (4–32 characters)
- **Link expiry** via optional `expires_at` timestamp
- **User ownership** — links are owned or anonymous; deleting a user keeps their links intact
- **Click analytics** recorded per visit:
  - IP address, country, city
  - Device type, OS, browser, user agent
  - Referrer URL
  - Unique visitor tracking via hashed IDs
- **Aggregated counters** — `total_clicks` and `unique_clicks` maintained at the DB level with integrity constraints
- **Soft-delete** for both users and links (`is_active` flag)
- **Role-based users** — `ADMIN` and `USER` roles backed by a native PostgreSQL enum
- **Async throughout** — non-blocking I/O from HTTP handler to database

---

## Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| Language           | Python 3.13                         |
| Web framework      | FastAPI                             |
| HTTP server        | Granian (ASGI, Rust-based)          |
| Database           | PostgreSQL 18                       |
| ORM                | SQLAlchemy 2.0 (async)              |
| DB driver          | asyncpg                             |
| Migrations         | Alembic (async mode)                |
| Settings           | Pydantic v2 + pydantic-settings     |
| Dependency injection | Dishka                            |
| Package manager    | uv                                  |
| Linting/formatting | Ruff                                |
| Dependency audit   | deptry                              |
| Testing            | pytest + pytest-asyncio + testcontainers |
| Containerization   | Docker + Docker Compose             |
| CI                 | GitHub Actions                      |
| Task runner        | just                                |

---

## Project Layout

```
src/app/
  main/
    config/       Settings, env loading, logging configuration
    ioc/          Dependency injection providers
    maker.py      FastAPI application factory
    run.py        Granian import target
  core/           Domain logic and business rules
  inbound/        HTTP route handlers
  outbound/       PostgreSQL persistence layer
    models/       SQLAlchemy ORM models (users, links, clicks)
    alembic/      Database migrations

tests/
  unit/           Unit tests (fast, no external dependencies)
```

---

## Quick Start

### With Docker (recommended)

```bash
cp env.example .env
# fill in POSTGRES_* values in .env

docker compose up --build
```

The service starts on `http://127.0.0.1:8000`.

| Endpoint            | URL                                     |
|---------------------|-----------------------------------------|
| Interactive API docs | `http://127.0.0.1:8000/docs`           |
| OpenAPI schema      | `http://127.0.0.1:8000/openapi.json`   |

Stop everything:

```bash
docker compose down
```

### Locally

```bash
cp env.example .env
uv sync

PYTHONPATH=src granian app.main.run:make_app \
  --factory --interface asgi --host 0.0.0.0 --port 8000 --reload
```

Run migrations after starting the database:

```bash
PYTHONPATH=src uv run alembic upgrade head
```

---

## Environment Variables

Copy the example and adjust:

```bash
cp env.example .env
```

### Application

| Variable               | Default        | Description                              |
|------------------------|----------------|------------------------------------------|
| `APP_SERVICE_NAME`     | `Best-Shorter` | Displayed in API docs                    |
| `APP_SERVICE_VERSION`  | `dev`          | `dev` or `prod`                          |
| `APP_DEBUG`            | `false`        | FastAPI debug mode                       |
| `APP_LOGGING_LEVEL`    | `INFO`         | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `APP_ROOT_PATH`        | `/`            | ASGI root path — useful behind a proxy   |

### Database

| Variable            | Default | Description             |
|---------------------|---------|-------------------------|
| `POSTGRES_DB`       | —       | Database name           |
| `POSTGRES_HOST`     | —       | `db_pg` inside Docker   |
| `POSTGRES_PORT`     | `5432`  |                         |
| `POSTGRES_USER`     | —       |                         |
| `POSTGRES_PASSWORD` | —       |                         |

### Connection Pool (SQLAlchemy)

| Variable           | Default | Description                           |
|--------------------|---------|---------------------------------------|
| `SQLA_ECHO`        | `false` | Log SQL statements                    |
| `SQLA_POOL_SIZE`   | `15`    | Persistent connections in the pool    |
| `SQLA_MAX_OVERFLOW`| `10`    | Burst connections beyond the pool     |

---

## Quality Checks

```bash
# Run tests
uv run pytest -v
# or
just test

# Lint, format, dependency audit
uv run ruff check --fix
uv run ruff format
uv run deptry
# or
just lint

# Everything at once
just check
```

Integration tests spin up a real PostgreSQL instance via testcontainers and are excluded from the default run. To include them:

```bash
uv run pytest -v -m integration
```

---

## Notes

- The project uses a `src` layout. Local commands require `PYTHONPATH=src`; Docker sets this automatically.
- The application is served by Granian over the ASGI interface.
- Alembic migration files are automatically linted by Ruff after generation.
- `APP_SERVICE_VERSION=prod` in the Docker build excludes dev dependencies from the final image.
