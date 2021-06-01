import json
import yaml
import pytest
import shutil
import os

from os.path import join, exists

from terraform_registry_api.terraform_module_registry_api.backends \
    import Filesystem
from terraform_registry_api.terraform_module_registry_api.exceptions \
    import ModuleNotFoundException

def generate_metadata(basedir, namespace, name):
    filename = join(basedir, namespace, name, "module_metadata.yaml")
    if not exists(filename):
        with open(filename, mode="wt") as modulefile:
            data = {
                "namespace": namespace,
                "name": name,
                "owner": "A. Person",
                "description": "A Module"
            }
            yaml.dump(data, modulefile)



@pytest.fixture
def backend():
    os.makedirs("./tests/backend/modules/namespace1/sample1/gcp/1.0.0/", exist_ok=True)
    os.mknod("./tests/backend/modules/namespace1/sample1/gcp/1.0.0/namespace1_sample1-gcp-1.0.0.tar.gz")
    os.makedirs("./tests/backend/modules/namespace1/sample1/aws/1.0.0/", exist_ok=True)
    os.mknod("./tests/backend/modules/namespace1/sample1/aws/1.0.0/namespace1_sample1-aws-1.0.0.tar.gz")
    os.makedirs("./tests/backend/modules/namespace1/sample1/aws/1.1.0/", exist_ok=True)
    os.mknod("./tests/backend/modules/namespace1/sample1/aws/1.1.0/namespace1_sample1-aws-1.1.0.tar.gz")
    os.makedirs("./tests/backend/modules/namespace1/sample1/aws/2.0.0/", exist_ok=True)
    os.mknod("./tests/backend/modules/namespace1/sample1/aws/2.0.0/namespace1_sample1-aws-2.0.0.tar.gz")
    os.makedirs("./tests/backend/modules/namespace1/sample2/aws/1.0.0/", exist_ok=True)
    os.mknod("./tests/backend/modules/namespace1/sample1/aws/1.0.0/namespace1_sample2-aws-1.0.0.tar.gz")
    os.makedirs("./tests/backend/modules/namespace1/sample2/aws/2.0.0/", exist_ok=True)
    os.mknod("./tests/backend/modules/namespace1/sample1/aws/1.0.0/namespace1_sample2-aws-2.0.0.tar.gz")
    generate_metadata("./tests/backend/modules/", "namespace1", "sample1")
    generate_metadata("./tests/backend/modules/", "namespace1", "sample2")
    yield Filesystem("./tests/backend/modules")
    shutil.rmtree("./tests/backend/modules")


def test_download_module_valid(backend):
    link = backend.download_version("namespace1", "sample1", "aws", "2.0.0")
    assert link == "namespace1/sample1/aws/2.0.0/namespace1_sample1-aws-2.0.0.tar.gz"


def test_download_module_notvalid(backend):
    with pytest.raises(ModuleNotFoundException):
        backend.download_version("nonamespace1", "sample1", "aws", "2.0.0")


def test_download_module_valid_no_version(backend):
    with pytest.raises(ModuleNotFoundException):
        backend.download_version("namespace1", "sample1", "aws", "3.0.0")


def test_get_versions_valid(backend):
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
    response_versions = backend.get_versions("namespace1", "sample1", "aws")
    assert response_versions == json.dumps(versions)


def test_get_versions_invalid(backend):
    with pytest.raises(ModuleNotFoundException):
        backend.get_versions("nonamespace1", "sample1", "aws")


def test_download_latest_modulefound(backend):
    response = backend.download_latest('http://localhost/', 'namespace1','sample1','aws')
    assert response == "http://localhost/v1/modules/namespace1/sample1/aws/2.0.0/download"


def test_download_latest_modulenotfound(backend):
    with pytest.raises(ModuleNotFoundException):
        backend.download_latest('http://localhost/', 'namespace1', 'sample1', 'aws2')


def test_get_all_modules(backend):
    details = {
        'meta': {
            'limit': 0,
            'current_offset': 0,
        },
        'modules': [
            {
                'id': '/namespace1/sample1/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            },
            {
                'id': '/namespace1/sample2/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'sample2',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample2/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }
    response = backend.get_modules("http://localhost/")

    assert json.loads(response) == details

def test_get_all_namespace1_modules(backend):
    details = {
        'meta': {
            'limit': 0,
            'current_offset': 0,
        },
        'modules': [
            {
                'id': '/namespace1/sample1/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            },
            {
                'id': '/namespace1/sample2/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'sample2',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample2/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }
    response = backend.get_modules("http://localhost/", "namespace1")

    assert json.loads(response) == details


def test_get_none_namespace2_modules(backend):
    details = {
        'meta': {
            'limit': 0,
            'current_offset': 0,
        },
        'modules': []
    }
    response = backend.get_modules("http://localhost/", "namespace2")

    assert json.loads(response) == details


def test_search_module_1result(backend):
    response = backend.search_modules("http://localhost/", "namespace1/sample1/aws")
    expected = {
        "meta": {
            "limit": 0,
            "current_offset": 0,
        },
        "modules": [
            {
                'id': '/namespace1/sample1/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }

    assert json.loads(response) == expected


def test_search_module_0result(backend):
    response = backend.search_modules("http://localhost/", "/namespace2/sample1/aws")
    expected = {
        'meta': {
            'limit': 0,
            'current_offset': 0,
        },
        'modules': []
    }
    assert json.loads(response) == expected


def test_search_module_2result(backend):
    response = backend.search_modules("http://localhost/", "/namespace1")
    expected = {
        "meta": {
            "limit": 0,
            "current_offset": 0,
        },
        "modules": [
            {
                'id': '/namespace1/sample1/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'test',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            },
            {
                'id': '/namespace1/sample2/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'sample2',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample2/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }
    assert json.loads(response) == expected


def test_get_latest_for_all_found(backend):
    response = backend.get_latest_all_providers("http://localhost/", "namespace1", "sample1")
    expected = {
        "meta": {
            "limit": 0,
            "current_offset": 0,
        },
        "modules": [
            {
                'id': '/namespace1/sample1/aws/2.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'sample1',
                'version': '2.0.0',
                'provider': 'aws',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            },
            {
                'id': '/namespace1/sample1/gcp/1.0.0',
                'owner': 'A. Person',
                'namespace': 'namespace1',
                'name': 'sample1',
                'version': '1.0.0',
                'provider': 'gcp',
                'description': 'A Module',
                'source': 'http://localhost/dl/modules/namespace1/sample1/gcp/1.0.0',
                'published_at': '2021-10-17T01:22:17.792066Z',
                'downloads': 213,
                'verified': True
            }
        ]
    }

    assert json.loads(response) == expected


def test_get_latest_for_all_notfound(backend):
    response = backend.get_latest_all_providers("http://localhost/", "namespace2", "sample1")
    expected = {
        'meta': {
            'limit': 0,
            'current_offset': 0,
        },
        'modules': []
    }

    assert json.loads(response) == expected


def test_get_latest_for_provider_found(backend):
    response = backend.get_module("http://localhost/", "namespace1", "sample1", "aws")
    expected = {
        "id": "namespace1/sample1/aws/2.0.0",
        "owner": "A. Person",
        "namespace": "namespace1",
        "name": "sample1",
        "version": "2.0.0",
        "provider": "aws",
        'description': 'A Module',
        'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
        'published_at': '2021-10-17T01:22:17.792066Z',
        'downloads': 213,
        "verified": True,
        "root": {
            "path": "",
            "readme": "# Title",
            "empty": False,
            "inputs": [
            ],
            "outputs": [
            ],
            "dependencies": [],
            "resources": []
        },
        "submodules": [
        ],
        "providers": [
            "aws",
            "gcp"
        ],
        "versions": [
            "1.0.0",
            "1.1.0",
            "2.0.0"
        ]
    }

    assert json.loads(response) == expected


def test_get_latest_for_provider_notfound(backend):
    with pytest.raises(ModuleNotFoundException):
        backend.get_module("http://localhost/", "namespace2", "sample1", "aws")


def test_get_module_details_notfound(backend):
    with pytest.raises(ModuleNotFoundException):
        backend.get_module("http://localhost/", "namespace2", "sample1", "aws", "2.0.0")


def test_get_module_details_found(backend):
    response = backend.get_module("http://localhost/", "namespace1", "sample1", "aws", "2.0.0")
    expected = {
        "id": "namespace1/sample1/aws/2.0.0",
        "owner": "A. Person",
        "namespace": "namespace1",
        "name": "sample1",
        "version": "2.0.0",
        "provider": "aws",
        'description': 'A Module',
        'source': 'http://localhost/dl/modules/namespace1/sample1/aws/2.0.0',
        'published_at': '2021-10-17T01:22:17.792066Z',
        'downloads': 213,
        "verified": True,
        "root": {
            "path": "",
            "readme": "# Title",
            "empty": False,
            "inputs": [
            ],
            "outputs": [
            ],
            "dependencies": [],
            "resources": []
        },
        "submodules": [
        ],
        "providers": [
            "aws",
            "gcp"
        ],
        "versions": [
            "1.0.0",
            "1.1.0",
            "2.0.0"
        ]
    }

    assert json.loads(response) == expected
