install:
	poetry install

test:
	poetry run pytest

build:
	poetry build

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml