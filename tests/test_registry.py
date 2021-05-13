import json
import pytest

from terraform_registry_api import registry


@pytest.fixture
def client():
    app = registry.create_app()
    app.app.testing = True
    yield app.app.test_client()


def test_service_discovery_endpoint(client):
    """Start with a blank database."""
    services = {
        "modules.v1": "http://localhost:5000/v1/modules",
        "providers.v1": "http://localhost:5000/v1/providers"
    }
    rv = client.get('/.well-known/terraform.json')
    assert rv.status_code == 200
    print(rv.data)
    assert json.loads(rv.data) == services
