init::
	pip install --upgrade pip
	pip install -r requirements.txt

black:
	black .

black-check:
	black --check .

flake8:
	flake8 --exclude .venv,node_modules

isort:
	isort --profile black .
