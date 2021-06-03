import json
import pytest

from os import remove, environ

from terraform_registry_api import registry


@pytest.fixture
def client():
    app = registry.create_app()
    app.testing = True
    yield app.test_client()


def test_service_discovery_endpoint(client):
    """Start with a blank database."""
    services = {
        "modules.v1": "http://localhost/v1/modules",
        "providers.v1": "http://localhost/v1/providers"
    }
    rv = client.get('/.well-known/terraform.json')
    assert rv.status_code == 200
    assert json.loads(rv.data) == services


def test_download_module_found(client):
    rv = client.get('/dl/module/terra/test/aws/2.0.0/test-2.0.0.tar.gz')
    assert rv.status_code == 200
    assert rv.content_type == "application/x-tar"
    remove("/tmp/test-2.0.0.tar.gz")
    remove("/tmp/notsupported.txt")


def test_download_module_notfound(client):
    rv = client.get('/dl/module/terra/notest/aws/2.0.0/test-2.0.0.zip')
    assert rv.status_code == 404
    assert rv.content_type == "application/problem+json"
    error = {
        "detail": "The requested file was not found on the server.",
        "status": 404,
        "title": "File Not Found",
        "type": "about:blank"
    }
    assert json.loads(rv.data) == error


def test_download_provider_not_supported(client):
    rv = client.get('/dl/provider/terra/test/aws/2.0.0/test-2.0.0.zip')
    assert rv.status_code == 500
    assert rv.content_type == "application/problem+json"
    error = {
        "detail": "The provider type is not yet supported",
        "status": 500,
        "title": "Not Yet Supported",
        "type": "about:blank"
    }
    assert json.loads(rv.data) == error


def test_download_test_not_a_thing(client):
    rv = client.get('/dl/test/terra/notest/aws/2.0.0/test-2.0.0.zip')
    assert rv.status_code == 400
    assert rv.content_type == "application/problem+json"
    error = {
        "detail": "Type is not valid: Valid Types are [module|provider]",
        "status": 400,
        "title": "Bad Request",
        "type": "about:blank"
    }
    assert json.loads(rv.data) == error


def test_fs_type():
    environ["fs_path"] = "./tests"
    app = registry.create_app()
    app.testing = True
    client = app.test_client()
    rv = client.get('/dl/module/terra/test/aws/2.0.0/test-2.0.0.zip')
    assert rv.status_code == 404
    assert rv.content_type == "application/problem+json"
    error = {
        "detail": "The requested file was not found on the server.",
        "status": 404,
        "title": "File Not Found",
        "type": "about:blank"
    }
    assert json.loads(rv.data) == error