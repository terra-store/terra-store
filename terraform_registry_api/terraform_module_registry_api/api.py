from terraform_registry_api.terraform_module_registry_api.backends import dummy as backend
from terraform_registry_api.terraform_module_registry_api.exceptions import ModuleNotFoundException
from flask import make_response

def list_versions(namespace, name, provider):
   try:
      return backend.get_versions(namespace, name, provider)
   except ModuleNotFoundException as e:
      return make_response(e.message, 404)

def download_version(namespace, name, provider, version):
   try:
      resp = make_response('', 204)
      resp.headers['X-Terraform-Get'] = backend.download_version(namespace, name, provider, version)
      return resp
   except ModuleNotFoundException as e:
      return make_response(e.message, 404)