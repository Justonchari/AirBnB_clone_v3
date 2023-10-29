#!/usr/bin/python3

"""create a route /status on the object app_views
that returns a JSON: "status": "OK" """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"])
def api_status():
    """returns JSON status"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats", methods=["GET"])
def api_stats():
    """Get api object stats"""

    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    # for klass in classes:
    #     objects_count[klass.__qualname__] = storage.count(klass)
    # return objects_count
    return jsonify({
        classes[klass]: storage.count(klass) for klass in classes
    })
