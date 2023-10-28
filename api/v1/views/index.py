#!/usr/bin/python3

"""create a route /status on the object app_views
that returns a JSON: "status": "OK" """


from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"])
def api_status():
    """returns JSON status"""
    response = {"status": "OK"}
    return jsonify(response)
