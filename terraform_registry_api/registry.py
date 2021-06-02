import json
import connexion

from connexion.exceptions import NonConformingResponse, BadRequestProblem, \
    ResolverProblem
from flask.helpers import send_file

from .terraform_module_registry_api import api
from .terraform_module_registry_api.exceptions import FileNotFoundException


def create_app():
    """Create and configure Flask API.

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
        """Service Discovery Endpoint.

        Returns:
            json: Descprion of the supported apis and the base urls
        """
        services = {
            "modules.v1": "http://localhost:5000/v1/modules",
            "providers.v1": "http://localhost:5000/v1/providers"
        }
        return json.dumps(services)

    @app.route("/dl/<type>/<path:filepath>")
    def download_files(type, filepath):
        if type == "module":
            try:
                requested = api.download_module(filepath)
            except FileNotFoundException:
                raise ResolverProblem(
                    status=404,
                    title="File Not Found",
                    detail="The requested file was not found on the server.")
        elif type == "provider":
            raise NonConformingResponse(
                reason="Not Yet Supported",
                message="The provider type is not yet supported")
        else:
            raise BadRequestProblem(
                detail="Type is not valid: Valid Types are [module|provider]")
        return send_file(requested)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
