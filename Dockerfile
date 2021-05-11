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

ADD . .
COPY --from=build /dist/terraform_registry_api-*-py3-none-any.whl /tmp/
RUN pip install -r test-requirements.txt && \
    pip install /tmp/terraform_registry_api*.whl

RUN coverage run --source=terraform_registry_api -m pytest tests/ && \
coverage report -m
ARG codecov_token=False
ENV codecov_token=$codecov_token
RUN apk add curl bash git && \
    if [ "$codecov_token" != "False" ]; then curl -o covbash https://codecov.io/bash; /bin/bash ./covbash; fi

FROM python:3.9-alpine as runtime

COPY prod-requirements.txt /tmp/
COPY --from=test /tmp/terraform_registry_api-*-py3-none-any.whl /tmp/
RUN pip install -r /tmp/prod-requirements.txt && \
    pip install /tmp/terraform_registry_api*.whl

CMD [ "/usr/local/bin/waitress-serve", "--call", "terraform_registry_api.registry:create_app" ]

