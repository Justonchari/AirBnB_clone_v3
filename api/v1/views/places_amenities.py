#!/usr/bin/python3
"""API endpoints for place amenities objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route(
    "/places/<place_id>/amenities",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def get_place_amenities(place_id):
    """Get all place amenities"""
    place = storage.get(cls="Place", id=place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        all_place_amenities = place.amenities
        return (
            jsonify([amenity.to_dict() for amenity in all_place_amenities]),
            200,
        )


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE", "POST"],
    strict_slashes=False,
)
def get_place_amenity(place_id, amenity_id):
    """Delete/Add place amenity by id"""
    place = storage.get(cls="Place", id=place_id)
    if place is None:
        abort(404)
    amenity = storage.get(cls="Amenity", id=amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "DELETE":
        if amenity not in place.amenities:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            place.save()
            return jsonify({}), 201
