package_name = dashboard_backend
repository = toolen/dashboard_backend
version = $(shell poetry version -s)
tag = $(repository):$(version)
hadolint_version=2.8.0
trivy_version=0.23.0

fmt:
	poetry run black .
	poetry run isort .
fmt-check:
	poetry run black . --check
	poetry run isort . --check
pre-commit:
	make fmt
	make lint
ci:
	make fmt-check
	make lint
lint:
	poetry run flake8 --ignore=E501 $(package_name)/ tests/
	make mypy
	poetry run pydocstyle $(package_name)/
	make test
	poetry run bandit -r $(package_name)
	poetry run safety check
	make radon
mypy:
	poetry run mypy $(package_name)
test:
	poetry run pytest -vv --cov=$(package_name) tests/
radon:
	poetry run radon cc --min C $(package_name)
	poetry run radon mi --min B $(package_name)
	poetry run radon raw --summary $(package_name) | tail -n12
