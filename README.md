# Best-Shorter

Best-Shorter is a FastAPI service for a URL shortener.

The project currently contains the application bootstrap, environment settings,
logging setup, Docker runtime, and test/lint tooling.

## Stack

- Python 3.13
- FastAPI
- Granian
- Pydantic Settings
- uv
- Docker Compose
- pytest
- Ruff

## Project Layout

```text
src/app/
  main/
    config/      Application settings and env loading
    maker.py     FastAPI app factory
    run.py       Granian import target
  core/          Domain code
  inbound/       API/input adapters
  outbound/      Persistence/output adapters
tests/
  unit/          Unit tests
```

## Environment

Copy the example file and adjust values if needed:

```bash
cp env.example .env
```

Available variables:

```env
GRANIAN_PORT=8000

APP_SERVICE_NAME=Best-Shorter
APP_SERVICE_VERSION=dev
APP_DEBUG=false
APP_LOGGING_LEVEL=INFO
APP_ROOT_PATH=/
```

`APP_LOGGING_LEVEL` can be one of:

```text
DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Run With Docker

Build and start the service:

```bash
docker compose up --build
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

Open the OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

Stop the service:

```bash
docker compose down
```

## Run Locally

Install dependencies:

```bash
uv sync
```

Start the app:

```bash
PYTHONPATH=src granian app.main.run:make_app --factory --interface asgi --host 0.0.0.0 --port 8000 --reload
```

## Quality Checks

Run tests:

```bash
uv run pytest -v
```

Run linting and formatting:

```bash
uv run ruff check --fix
uv run ruff format
uv run deptry
```

If `just` is installed, the same checks are available as:

```bash
just test
just lint
just check
```

## Notes

- The package uses a `src` layout, so local commands must run with
  `PYTHONPATH=src` unless the project is installed into the active environment.
- Docker sets `PYTHONPATH=/code/src` automatically.
- The application is served by Granian using the ASGI interface.
