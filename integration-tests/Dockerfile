FROM hashicorp/terraform:light

ADD terraform /terraform
ADD ./nginx/cert.pem /usr/local/share/ca-certificates

RUN update-ca-certificates

WORKDIR /terraform