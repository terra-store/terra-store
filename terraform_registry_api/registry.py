import json
import connexion
from flask import request, make_response
from werkzeug.middleware.proxy_fix import ProxyFix

from connexion.exceptions import NonConformingResponse, BadRequestProblem, \
    ResolverProblem
from flask.helpers import send_file
from os import environ

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
    app.app.wsgi_app = ProxyFix(app.app.wsgi_app)

    if environ.get("fs_path") is not None:
        api.set_backend("Filesystem")

    # Read the swagger.yml file to configure the endpoints
    app.add_api("terraform_module_registry_api/swagger.yml")

    @app.route("/.well-known/terraform.json")
    def service_discovery():
        """Service Discovery Endpoint.

        Returns:
            json: Descprion of the supported apis and the base urls
        """
        print(request.url)
        services = {
            "modules.v1": "{root}v1/modules".format(root=request.url_root),
            "providers.v1": "{root}v1/providers".format(root=request.url_root)
        }
        resp = make_response(json.dumps(services), 200)
        resp.content_type = "application/json"
        return resp

    @app.route("/dl/<modtype>/<path:filepath>")
    def download(modtype, filepath):
        if modtype == "module":
            try:
                requested = api.download_module(filepath)
            except FileNotFoundException:
                raise ResolverProblem(
                    status=404,
                    title="File Not Found",
                    detail="The requested file was not found on the server.")
        elif modtype == "provider":
            raise NonConformingResponse(
                reason="Not Yet Supported",
                message="The provider type is not yet supported")
        else:
            raise BadRequestProblem(
                detail="Type is not valid: Valid Types are [module|provider]")
        return send_file(requested)

    return app.app
