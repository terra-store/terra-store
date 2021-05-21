build: ## Builds the terra-store wheel
	pip install -r requirements.txt
	python3 -m build

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage

lint: ## Lint the project
	flake8 --exclude=venv,build
 
test: build ## Run all test packages
	pip install -r test-requirements.txt
	coverage run --source=terraform_registry_api -m pytest tests/
	coverage report -m
	coverage xml

run: ## Run local version of flask app 
	python3 terraform_registry_api/registry.py

production: build test ## Build production container
	docker build \
	  --file=./Dockerfile \
	  --tag=test .

prod-run: production ## Runs production container with port 8080 mapped
	docker run -d -p 8080:8080 test:latest

help: ## Display this help text
	@echo "Usage: make <target>"
	@echo ""
	@echo Available Targets:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
