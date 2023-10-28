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
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = [Amenity, City, Place, Review, State, User]
    # for klass in classes:
    #     objects_count[klass.__qualname__] = storage.count(klass)
    # return objects_count
    return {klass.__qualname__.lower():
            storage.count(klass) for klass in classes}
