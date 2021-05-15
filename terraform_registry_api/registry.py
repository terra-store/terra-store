import json
import connexion


def create_app():
    """Create and configure Flask API

    Create and configure the Flask API using theswagger defnitions

    Returns:
        FlaskApp: The intialized FlaskApp Server
    """
    # Create the application instance
    app = connexion.App(__name__, specification_dir="./")

    # Read the swagger.yml file to configure the endpoints
    app.add_api("terraform_module_registry_api/swagger.yml")

    @app.route("/.well-known/terraform.json")
    def service_discovery():
        """Service Discovery Endpoint

        Returns:
            json: Descprion of the supported apis and the base urls
        """
        services = {
            "modules.v1": "http://localhost:5000/v1/modules",
            "providers.v1": "http://localhost:5000/v1/providers"
        }
        return json.dumps(services)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
