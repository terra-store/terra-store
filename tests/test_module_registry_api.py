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
    assert rv.headers['X-Terraform-Get'] == \
        "https://api.github.com/repos/pexa/aws-test/v2.0.0"


def test_download_module_versionnotfound(client):
    rv = client.get('/v1/modules/pexa/test/aws/2.1.0/download')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /pexa/test/aws'


def test_download_module_namenotfound(client):
    rv = client.get('/v1/modules/pexa/test/aws2/2.1.0/download')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /pexa/test/aws2'


def test_list_versions_valid(client):
    rv = client.get('/v1/modules/pexa/test/aws/versions')
    assert rv.status_code == 200


def test_list_versions_modulenotfound(client):
    rv = client.get('/v1/modules/pexa/test/aws2/versions')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /pexa/test/aws2'


def test_download_latest_modulefound(client):
    rv = client.get('/v1/modules/pexa/test/aws/download')
    assert rv.status_code == 302
    assert rv.headers['Location'] == \
        "http://localhost:5000/v1/modules/pexa/test/aws/2.0.0/download"


def test_download_latest_modulenotfound(client):
    rv = client.get('/v1/modules/pexa/test/aws2/download')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /pexa/test/aws2'
