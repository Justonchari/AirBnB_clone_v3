#!/usr/bin/python3
"""API endpoints for amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
def get_amenities():
    """Get all amenites"""

    if request.method == "GET":
        amenities = storage.all(cls="Amenity")
        return (
            jsonify([amenity.to_dict() for amenity_id,
                     amenity in amenities.items()]),
            200,
        )

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        if not data.get("name", None):
            return jsonify({"error": "Missing name"}), 400
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get/Delete/Update amenity by id"""
    amenity = storage.get(cls="Amenity", id=amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        for k, v in data.items():
            if k not in {"id", "created_at", "updated_at"}:
                setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
