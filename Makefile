build: ## Builds the terra-store wheel
	pip install -r requirements.txt
	python3 -m build

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage

lint: ## Lint the project
	flake8
	cd terraform_registry_api; pydocstyle; cd -
 
test: build ## Run all test packages
	pip install -r test-requirements.txt
	coverage run --source=terraform_registry_api -m pytest tests/
	coverage report -m
	coverage xml

ssl: ## generate self-signed certificate
	openssl req -subj '/CN=proxy.ts.int' \
    -x509 -newkey rsa:4096 -nodes \
    -keyout integration-tests/nginx/key.pem \
    -out integration-tests/nginx/cert.pem \
    -days 365 -extensions 'v3_req' \
    -reqexts san -extensions san \
    -config integration-tests/nginx/config.cnf

integration-tests: ssl ## Run integration tests
	./integration-tests/test.sh

debug: ## Run local version of flask app 
	FLASK_APP=terraform_registry_api/registry.py:create_app FLASK_ENV=development flask run

container: build test ## Build local container
	docker build \
	  --file=./Dockerfile \
	  --tag=test .

run: production ## Run container with port 8080 mapped
	docker run -d -p 8080:8080 test:latest

help: ## Display this help text
	@echo "Usage: make <target>"
	@echo ""
	@echo Available Targets:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
