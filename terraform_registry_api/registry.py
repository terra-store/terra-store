import connexion
import json


def create_app():
    # Create the application instance
    app = connexion.App(__name__, specification_dir="./")

    # Read the swagger.yml file to configure the endpoints
    app.add_api("terraform_module_registry_api/swagger.yml")

    @app.route("/.well-known/terraform.json")
    def service_discovery():
        services = {
            "modules.v1": "http://localhost:5000/v1/modules",
            "providers.v1": "http://localhost:5000/v1/providers"
        }
        return json.dumps(services)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
