#!/usr/bin/python3

"""
This module create a variable app, instance of Flask and run at
HBNB_API_HOST and HBNB_API_PORT
"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def purge_session(request):
    """deletes a session after a request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """
    handles the page not found error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
