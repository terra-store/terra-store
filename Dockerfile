FROM python:3.9-alpine

COPY dist/terraform_registry_api-*-py3-none-any.whl /tmp/
RUN pip install flask==1.1.2 && \
    pip install connexion==2.7.0 && \
    pip install waitress==2.0.0 && \
    pip install /tmp/terraform_registry_api*.whl

CMD [ "/usr/local/bin/waitress-serve", "--call", "terraform_registry_api.registry:create_app" ]

