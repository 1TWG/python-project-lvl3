install:
	poetry install

check:
	poetry check

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --cov=page_loader --cov-report xml

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

page-loader:
	poetry run page-loader https://snipp.ru/demo/76/index.html

tpage-loader:
	poetry run page-loader https://ru.hexlet.io/courses


