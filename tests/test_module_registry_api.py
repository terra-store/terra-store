import json
import pytest

from terraform_registry_api import registry

@pytest.fixture
def client():
    app = registry.create_app()
    app.app.testing = True
    yield app.app.test_client()

def test_download_module_valid(client):
    rv = client.get('/v1/modules/pexa/test/aws/2.0.0/download')
    assert rv.status_code == 204


def test_download_module_versionnotfound(client):
    rv = client.get('/v1/modules/pexa/test/aws/2.1.0/download')
    assert rv.status_code == 404

def test_download_module_namenotfound(client):
    rv = client.get('/v1/modules/pexa/nonexistent/aws/2.1.0/download')
    assert rv.status_code == 404

def test_list_versions_valid(client):
    rv = client.get('/v1/modules/pexa/test/aws/versions')
    assert rv.status_code == 200

def test_list_versions_modulenotfound(client):
    rv = client.get('/v1/modules/pexa/test/aws2/versions')
    assert rv.status_code == 404