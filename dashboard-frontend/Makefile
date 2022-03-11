package_name = dashboard_frontend
repository = toolen/dashboard-frontend
version = $(shell npm run version | tail -1)
image_tag = ghcr.io/$(repository):$(version)
hadolint_version=2.8.0
trivy_version=0.24.2

image:
	export DOCKER_BUILDKIT=1
	make hadolint
	docker build --pull --no-cache -t $(image_tag) .
	make trivy
	make size
container:
	docker run --cap-drop=ALL $(image_tag)
connect:
	docker run -it --cap-drop=ALL $(image_tag) /bin/bash
size:
	docker images | grep $(repository) | grep $(version)
hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile
trivy:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ~/.cache/trivy:/root/.cache/ aquasec/trivy:$(trivy_version) image --ignore-unfixed $(image_tag)
push-to-ghcr:
	docker login ghcr.io -u toolen -p $(CR_PAT)
	docker push $(image_tag)
ci:
	npm install
	npm install -g @lhci/cli@0.8.x
	npm run build
	lhci autorun
