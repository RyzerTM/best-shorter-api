lint:
    ruff check --fix
    ruff format
    deptry

test: 
    pytest -v --cov=. --cov-report=term-missing --cov-report=html

check: lint test
    coverage html