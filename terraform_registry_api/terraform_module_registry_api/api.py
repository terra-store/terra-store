from flask import make_response, redirect, request
from os import environ

from .backends import Dummy, Filesystem
from .exceptions import ModuleNotFoundException

backend = Dummy()


def list_modules(namespace=None):
    """List modules in namespace requested.

    Response format:
    {
        "meta": {
            "limit": 2,
            "current_offset": 0,
            "next_offset": 2,
            "next_url": "/v1/modules?limit=2&offset=2&verified=true"
        },
        "modules": [
            {
            "id": "GoogleCloudPlatform/lb-http/google/1.0.4",
            "owner": "",
            "namespace": "GoogleCloudPlatform",
            "name": "lb-http",
            "version": "1.0.4",
            "provider": "google",
            "description": "Description.",
            "source": "source_url",
            "published_at": "2017-10-17T01:22:17.792066Z",
            "downloads": 213,
            "verified": true
            },
            {
            "id": "terraform-aws-modules/vpc/aws/1.5.1",
            "owner": "",
            "namespace": "terraform-aws-modules",
            "name": "vpc",
            "version": "1.5.1",
            "provider": "aws",
            "description": "TDescription",
            "source": "source_url",
            "published_at": "2017-11-23T10:48:09.400166Z",
            "downloads": 29714,
            "verified": true
            }
        ]
    }

    Args:
        namespace (str, optional): Namespace for the module. Defaults to None.

    Returns:
        response: JSON formatted respnse
    """
    return make_response(backend.get_modules(request.url_root, namespace), 200)


def list_all_modules():
    """List all modules.

    See list_modules for details.

    Returns:
        response: json list of all modules
    """
    return list_modules()


def list_versions(namespace, name, provider):
    """List version for mnodule.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module

    Returns:
        response: JSON formatted respnse
    """
    try:
        return make_response(backend.get_versions(namespace, name, provider),
                             200)
    except ModuleNotFoundException as module_not_found:
        return make_response(module_not_found.message, 404)


def download_version(namespace, name, provider, version):
    """Download url for module release.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module
        version (str): Version for the module

    Returns:
        response: JSON formatted respnse
    """
    try:
        resp = make_response('', 204)
        artifact = backend.download_version(
            namespace, name, provider, version)
        if artifact.startswith("http"):
            final_artifact = artifact
        else:
            final_artifact = "{root}dl/module/{artifact}".format(root=request.url_root,
                                                                 artifact=artifact)
        resp.headers['X-Terraform-Get'] = final_artifact
        return resp
    except ModuleNotFoundException as module_not_found:
        return make_response(module_not_found.message, 404)


def search_modules(q):
    """Search modules based on the query.

    Args:
        q (str, optional): Ther query string to search for. Defaults to None.

    Returns:
        response: list of modules matching the
                  relevant search query as json
    """
    return make_response(backend.search_modules(
        request.url_root, q), 200)


def get_latest_for_all_providers(namespace, name):
    """Get latest version for all providers.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module

    Returns:
        json: Details of vesion for each provider
    """
    return make_response(
        backend.get_latest_all_providers(request.url_root, namespace, name),
        200)


def get_latest_for_provider(namespace, name, provider):
    """Get Latest version for Provider.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module

    Returns:
        response: JSON formatted respnse
    """
    try:
        return make_response(backend.get_module(
            request.url_root, namespace, name, provider), 200)
    except ModuleNotFoundException as module_not_found:
        return make_response(module_not_found.message, 404)


def get_module(namespace, name, provider, version):
    """Get Module Details.

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module
        version (str): Version for the module

    Returns:
        response: JSON formatted respnse
    """
    try:
        return make_response(
            backend.get_module(
                request.url_root, namespace, name, provider, version),
            200)
    except ModuleNotFoundException as module_not_found:
        return make_response(module_not_found.message, 404)


def download_latest(namespace, name, provider):
    """Download Latest Module.

    Download the latest version of the odule,
    returning 302 to version download.
    Raise 404 if module not found

    Args:
        namespace (str): namespace for the version
        name (str): Name of the module
        provider (str): Provider for the module

    Returns:
        response: JSON formatted respnse
    """
    try:
        return redirect(backend.download_latest(
            request.url_root, namespace, name, provider))
    except ModuleNotFoundException as module_not_found:
        return make_response(module_not_found.message, 404)


def download_module(filepath):
    """Download the module at the requested filepath.

    Args:
        filepath (str): path to requested file

    Returns:
        filestream: binary representation of file requested
    """
    return backend.download_module(filepath)


def set_backend(backendtype):
    """Set backend.

    Args:
        backendtype (str): Type of backend requested
    """
    if backendtype == "Filesystem":
        global backend
        backend = Filesystem(environ.get("fs_path"))
