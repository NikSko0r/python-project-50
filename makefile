install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 brain_games

reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl
