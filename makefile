install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint
