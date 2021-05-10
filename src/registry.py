from flask import render_template
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

# @app.errorhandler(404)
# def page_not_found(e):
#     return "{\"error\": \"Module Not Found\"}", 404

if __name__ == "__main__":
    app.run(debug=True)