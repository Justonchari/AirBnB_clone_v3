#!/usr/bin/python3
"""API endpoints for place objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route(
    "/cities/<city_id>/places", methods=["GET", "POST"], strict_slashes=False
)
def get_city_places(city_id):
    """Get all city places, Create place"""
    city = storage.get(cls="City", id=city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        all_city_places = city.places
        return jsonify([place.to_dict() for place in all_city_places]), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        user_id = data.get("user_id", None)
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400
        elif not storage.get(cls="User", id=user_id):
            abort(404)
        elif not data.get("name", None):
            return jsonify({"error": "Missing name"}), 400
        new_place = Place(city_id=city_id, **data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route(
    "/places/<place_id>", methods=["GET", "DELETE", "PUT"],
    strict_slashes=False
)
def get_place(place_id):
    """Get/Delete/Update place by id"""
    place = storage.get(cls="Place", id=place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        for k, v in data.items():
            if k not in {"id", "created_at", "updated_at"}:
                setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
