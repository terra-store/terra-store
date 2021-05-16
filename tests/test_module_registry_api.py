import json
import pytest

from terraform_registry_api import registry


@pytest.fixture
def client():
    app = registry.create_app()
    app.app.testing = True
    yield app.app.test_client()


def test_download_module_valid(client):
    rv = client.get('/v1/modules/terra/test/aws/2.0.0/download')
    assert rv.status_code == 204
    assert rv.headers['X-Terraform-Get'] == \
        "https://api.github.com/repos/terra/aws-test/v2.0.0"


def test_download_module_versionnotfound(client):
    rv = client.get('/v1/modules/terra/test/aws/2.1.0/download')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra/test/aws'


def test_download_module_namenotfound(client):
    rv = client.get('/v1/modules/terra/test/aws2/2.1.0/download')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra/test/aws2'


def test_list_versions_valid(client):
    rv = client.get('/v1/modules/terra/test/aws/versions')
    versions = {
        "modules": [
            {
                "versions": [
                    {"version": "1.0.0"},
                    {"version": "1.1.0"},
                    {"version": "2.0.0"}
                ]
            }
        ]
    }
    assert rv.status_code == 200
    assert json.loads(rv.data) == json.dumps(versions)


def test_list_versions_modulenotfound(client):
    rv = client.get('/v1/modules/terra/test/aws2/versions')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra/test/aws2'


def test_download_latest_modulefound(client):
    rv = client.get('/v1/modules/terra/test/aws/download',
                    follow_redirects=False)
    assert rv.status_code == 302
    assert rv.headers['Location'] == \
        "http://localhost:5000/v1/modules/terra/test/aws/2.0.0/download"


def test_download_latest_modulenotfound(client):
    rv = client.get('/v1/modules/terra/test/aws2/download')
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra/test/aws2'


def test_get_all_modules(client):
    details = {
        'meta': {
            'limit': 1,
            'current_offset': 0,
        },
        'modules': [
            {
                'id': '/terra/test/aws/2.0.0',
                'owner': 'noone',
                'namespace': 'terra',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'Fake Module.',
                'source': 'http://localhost:5000/storage/terra/test/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }
    rv = client.get("/v1/modules/")
    assert rv.status_code == 200
    assert json.loads(rv.data) == details


def test_get_all_modules_limit2(client):
    details = {
        'meta': {
            'limit': 1,
            'current_offset': 0,
        },
        'modules': [
            {
                'id': '/terra/test/aws/2.0.0',
                'owner': 'noone',
                'namespace': 'terra',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'Fake Module.',
                'source': 'http://localhost:5000/storage/terra/test/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }
    rv = client.get("/v1/modules/?limit=2")
    assert rv.status_code == 200
    assert json.loads(rv.data) == details


def test_get_all_terra_modules(client):
    details = {
        'meta': {
            'limit': 1,
            'current_offset': 0,
        },
        'modules': [
            {
                'id': '/terra/test/aws/2.0.0',
                'owner': 'noone',
                'namespace': 'terra',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'Fake Module.',
                'source': 'http://localhost:5000/storage/terra/test/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }
    rv = client.get("/v1/modules/terra")
    assert rv.status_code == 200
    assert json.loads(rv.data) == details


def test_get_none_terra2_modules(client):
    details = {
        'meta': {
            'limit': 0,
            'current_offset': 0,
        },
        'modules': []
    }
    rv = client.get("/v1/modules/terra2")
    assert rv.status_code == 200
    assert json.loads(rv.data) == details


def test_search_module_1result(client):
    rv = client.get("/v1/modules/search?q=/terra/test/aws")
    assert rv.status_code == 200


def test_search_module_0result(client):
    rv = client.get("/v1/modules/search?q=/terra2/test/aws")
    assert rv.status_code == 200


def test_search_module_2result(client):
    rv = client.get("/v1/modules/search?q=/terra/test")
    assert rv.status_code == 200


def test_get_latest_for_all_found(client):
    rv = client.get("/v1/modules/terra/test")
    assert rv.status_code == 200


def test_get_latest_for_all_notfound(client):
    rv = client.get("/v1/modules/terra2/test")
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra2/test'


def test_get_latest_for_provider_found(client):
    rv = client.get("/v1/modules/terra/test/aws")
    assert rv.status_code == 200


def test_get_latest_for_provider_notfound(client):
    rv = client.get("/v1/modules/terra2/test/aws")
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra2/test/aws'


def test_get_module_details_notfound(client):
    rv = client.get("/v1/modules/terra2/test/aws/2.0.0")
    assert rv.status_code == 404
    assert rv.data == b'Module Not Found: /terra2/test/aws'


def test_get_module_details_found(client):
    rv = client.get("/v1/modules/terra/test/aws/2.0.0")
    assert rv.status_code == 200
