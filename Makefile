install:
	poetry install

test:
	poetry run pytest

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/hexlet_code-0.1.0-py3-none-any.whl

lint:
	poetry run flake8 page_loader

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml