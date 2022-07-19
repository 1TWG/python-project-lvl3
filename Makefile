install:
	poetry install

test:
	poetry run pytest --cov=page_loader/tests -vv --cov-report xml

.PHONY: install test lint check build

build:
	poetry build

publish:
	poetry publish --dry-run


lint:
	poetry run flake8 page_loader

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

package-install:
	python3 -m pip install .

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

page-loader:
	poetry run page-loader https://snipp.ru/demo/76/index.html

tpage-loader:
	poetry run page-loader https://ru.hexlet.io/courses


