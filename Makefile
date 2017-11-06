CONTAINER_NAME=a1exanderjung/trendt
CONTAINER_VERSION=0.1.0

.PHONY: container
container:
	docker build -t $(CONTAINER_NAME):$(CONTAINER_VERSION) \
		--network host \
		.

.PHONY: start
start: container
	docker run -it --rm \
		--name dockerfile-usage \
		--volume $(shell pwd):/app \
		--network host \
		$(CONTAINER_NAME):$(CONTAINER_VERSION)
