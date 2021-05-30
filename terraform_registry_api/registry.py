import json
import connexion
from flask import request, make_response
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    """Create and configure Flask API.

    Create and configure the Flask API using theswagger defnitions

    Returns:
        FlaskApp: The intialized FlaskApp Server
    """
    # Create the application instance
    app = connexion.App(__name__, specification_dir="./")
    app.app.wsgi_app = ProxyFix(app.app.wsgi_app)

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
        resp.content_type="application/json"
        return resp 
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
