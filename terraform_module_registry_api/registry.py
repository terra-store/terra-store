from flask import render_template
import connexion
import json

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

@app.route("/.well-known/terraform.json")
def service_discovery():
    services = {
        "modules.v1": "http://localhost:5000/v1/modules",
        "providers.v1": "http://localhost:5000/v1/providers",
        "login.v1": "http://localhost:5000/v1/login"
    }
    return json.dumps(services)

if __name__ == "__main__":
    app.run(debug=True)