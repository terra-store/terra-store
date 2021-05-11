FROM python:3.9-alpine

COPY prod-requirements.txt /tmp/
COPY dist/terraform_registry_api-*-py3-none-any.whl /tmp/
RUN pip install -r /tmp/prod-requirements.txt && \
    pip install /tmp/terraform_registry_api*.whl

CMD [ "/usr/local/bin/waitress-serve", "--call", "terraform_registry_api.registry:create_app" ]

