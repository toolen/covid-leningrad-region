package_name = scraper
repository = toolen/scraper
version = $(shell poetry version -s)
image_tag = ghcr.io/$(repository):$(version)
hadolint_version=2.12.0
trivy_version=0.43.1
pwd=$(shell pwd)

image:
	export DOCKER_BUILDKIT=1
	make hadolint
	docker build --pull --no-cache -t $(image_tag) .
	make trivy
	make size
image\:nocache:
	docker build --pull -t $(image_tag) .
	make trivy
image\:builder\:shell:
	docker build --target builder -t $(image_tag) .
	docker run -it -v $(pwd):/code $(image_tag) /bin/bash
container:
	docker run --cap-drop=ALL --dns=77.88.8.8 --dns=77.88.8.1 $(image_tag)
connect:
	docker run -it --cap-drop=ALL $(image_tag) /bin/ash
size:
	docker images | grep $(repository) | grep $(version)
hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile
trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ~/.cache/trivy:/root/.cache/ aquasec/trivy:$(trivy_version) image --ignore-unfixed $(image_tag)
push:
	docker trust sign $(image_tag)
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
	poetry run safety check -i 71608 -i 72236 -i 71064 -i 70626 -i 67895 -i 70612 -i 72083 -i 71591 -i 64227 -i 65401
	poetry run radon cc --min C $(package_name)
	poetry run radon mi --min B $(package_name)
	poetry run radon raw --summary $(package_name) | tail -n12
clear-cache:
	poetry cache clear pypi --all
email-server:
	python -m smtpd -n -c DebuggingServer localhost:1025
push-to-ghcr:
	docker login ghcr.io -u toolen -p $(CR_PAT)
	docker push $(image_tag)
.PHONY: docs
docs:
	make -C docs html
	python -m http.server 8000 --bind 127.0.0.1 --directory docs/build/html