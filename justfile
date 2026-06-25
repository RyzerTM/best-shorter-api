# Pytest
test:
    pytest -v --cov=. --cov-report=term-missing --cov-report=html

# Ruff
lint:
    ruff check --fix
    ruff format
    deptry

check: lint test
    coverage html
