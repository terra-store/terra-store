build:
	pip install -r requirements.txt
	python3 -m build

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage

lint:
	flake8 --exclude=.tox

test: build
	pip install -r test-requirements.txt
	coverage run --source=terraform_registry_api -m pytest tests/
	coverage report -m
	coverage xml

run:
	python3 terraform_registry_api/registry.py

prod-run: production
	docker run -d -p 8080 test:latest

production: build test
	docker build \
	  --file=./Dockerfile \
	  --tag=test .