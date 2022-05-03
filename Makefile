.PHONY: format lint cov

all: format lint cov

format:
	@echo Formating Python code
	black --exclude '/(\.direnv|\.pyenv)/' .
	isort --skip-glob .pyenv --profile black .

lint:
	@echo Linting Python code
	flake8 --exclude=.pyenv/,.direnv/ --ignore=E203,E501,W503
	isort --check-only --skip-glob .pyenv --profile black .
	black --check --exclude '/(\.direnv|\.pyenv)/' .

cov:
	coverage run --source='.' --omit '.pyenv/*' manage.py test
	coverage report -m

pginit:
	PGDATA=postgres-data/ pg_ctl init
	PGDATA=postgres-data/ pg_ctl start
	createuser illich
	psql -U ${USER} -d postgres -c "ALTER USER illich CREATEDB;"
	psql -U illich -d postgres -c "CREATE DATABASE illich;"

pgstart:
	PGDATA=postgres-data/ pg_ctl start

pgstop:
	PGDATA=postgres-data/ pg_ctl stop
