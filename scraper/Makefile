package_name = scraper
repository = toolen/scraper
version = $(shell poetry version -s)
tag = $(repository):$(version)
hadolint_version=2.8.0
trivy_version=0.21.1

image:
	make hadolint
	docker build --pull --no-cache -t $(tag) .
	make trivy
	make size
container:
	docker run -p 8080:8080 --cap-drop=ALL $(tag)
connect:
	docker run -it --cap-drop=ALL $(tag) /bin/bash
size:
	docker images | grep $(repository) | grep $(version)
hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile
trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ~/.cache/trivy:/root/.cache/ aquasec/trivy:$(trivy_version) $(tag)
push:
	docker trust sign $(tag)
mypy:
	poetry run mypy --ignore-missing-imports $(package_name)
pre-commit:
	poetry run black .
	poetry run isort .
	poetry run flake8 --ignore E501 $(package_name)/ tests/
	make mypy
	poetry run pydocstyle --add-ignore=D104 $(package_name)/
	poetry run pytest --cov=$(package_name) tests/
	poetry run bandit -r $(package_name)
	poetry run safety check
	poetry run radon cc $(package_name)
	poetry run radon mi $(package_name)
	poetry run radon raw $(package_name)
	poetry run radon hal $(package_name)
