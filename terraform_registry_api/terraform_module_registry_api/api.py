from terraform_module_registry_api.backends import dummy as backend
from flask import make_response

def list_versions(namespace, name, provider):
   return backend.get_versions(namespace, name, provider)

def download_version(namespace, name, provider, version):
    resp = make_response('', 204)
    resp.headers['X-Terraform-Get'] = backend.download_version(namespace, name, provider, version)
    return resp