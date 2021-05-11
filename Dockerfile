FROM python:3.9-alpine as build


ADD terraform_registry_api ./terraform_registry_api
COPY requirements.txt /tmp/
COPY MANIFEST.in .
COPY setup.py .
COPY pyproject.toml .
COPY LICENSE .
COPY README.md .

RUN pip install -r /tmp/requirements.txt
RUN python3 -m build

FROM  python:3.9-alpine as test

COPY test-requirements.txt /tmp/
COPY tests ./tests
COPY --from=build /dist/terraform_registry_api-*-py3-none-any.whl /tmp/
RUN pip install -r /tmp/test-requirements.txt && \
    pip install /tmp/terraform_registry_api*.whl

RUN coverage run --source=terraform_registry_api -m pytest tests/ && \
coverage report -m
ARG CI=False
ENV e_CI=$CI
RUN apk add curl bash && \
    if [ "$e_CI" == "True" ]; then curl -o covbash https://codecov.io/bash; /bin/bash ./covbash; fi

# FROM python:3.9-alpine as runtime

# COPY prod-requirements.txt /tmp/
# COPY --from=test /tmp/terraform_registry_api-*-py3-none-any.whl /tmp/
# RUN pip install -r /tmp/prod-requirements.txt && \
#     pip install /tmp/terraform_registry_api*.whl

# CMD [ "/usr/local/bin/waitress-serve", "--call", "terraform_registry_api.registry:create_app" ]

