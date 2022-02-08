package_name = scraper
repository = toolen/scraper
version = $(shell poetry version -s)
tag = $(repository):$(version)
hadolint_version=2.8.0
trivy_version=0.23.0

image:
	export DOCKER_BUILDKIT=1
	make hadolint
	docker build --pull --no-cache -t $(tag) .
	make trivy
	make size
container:
	docker run --cap-drop=ALL --dns=77.88.8.8 --dns=77.88.8.1 $(tag)
connect:
	docker run -it --cap-drop=ALL $(tag) /bin/ash
size:
	docker images | grep $(repository) | grep $(version)
hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile
trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ~/.cache/trivy:/root/.cache/ aquasec/trivy:$(trivy_version) image --ignore-unfixed $(tag)
push:
	docker trust sign $(tag)
mypy:
	poetry run mypy $(package_name)
test:
	poetry run pytest -vv --cov=$(package_name) tests/
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
	poetry run flake8 --ignore E501,W503 $(package_name)/ tests/
	make mypy
	poetry run pydocstyle --add-ignore=D104 $(package_name)/
	make test
	poetry run bandit -r $(package_name)
	poetry run safety check
	poetry run radon cc --min C $(package_name)
	poetry run radon mi --min B $(package_name)
	poetry run radon raw --summary $(package_name) | tail -n12
email-server:
	python -m smtpd -n -c DebuggingServer localhost:1025
#env:
#	export $(grep -v "^#" /home/toolen/Projects/covid-stat-priozersk/.env_local | xargs)