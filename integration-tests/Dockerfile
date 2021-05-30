FROM hashicorp/terraform:light

COPY terraform /terraform
COPY ./nginx/cert.pem /usr/local/share/ca-certificates

RUN update-ca-certificates

WORKDIR /terraform