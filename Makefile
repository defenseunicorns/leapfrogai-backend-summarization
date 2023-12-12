VERSION ?= $(shell git describe --abbrev=0 --tags)

create-venv:
	python -m venv .venv

activate-venv:
	source .venv/bin/activate

requirements-dev:
	python -m pip install -r requirements-dev.txt

requirements:
	pip-sync requirements.txt requirements-dev.txt

build-requirements:
	pip-compile -o requirements.txt pyproject.toml

build-requirements-dev:
	pip-compile --extra dev -o requirements-dev.txt pyproject.toml --allow-unsafe

test:
	pytest **/*.py

dev:
	uvicorn main:app --port 8081 --reload

docker-build:
	docker build -t ghcr.io/defenseunicorns/leapfrogai/summarization:${VERSION} .

docker-push:
	docker push ghcr.io/defenseunicorns/leapfrogai/summarization:${VERSION}