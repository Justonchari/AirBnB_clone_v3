#!/usr/bin/python3
"""API endpoints for city objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route(
    "/states/<state_id>/cities", methods=["GET", "POST"], strict_slashes=False
)
def get_state_cities(state_id):
    """Get all state cities, Create city"""
    state = storage.get(cls="State", id=state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        all_state_cities = state.cities
        return jsonify([city.to_dict() for city in all_state_cities]), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        if not data.get("name", None):
            return jsonify({"error": "Missing name"}), 400
        new_city = City(state_id=state_id, **data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route(
    "/cities/<city_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False
)
def get_city(city_id):
    """Get/Delete/Update city by id"""
    city = storage.get(cls="City", id=city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        for k, v in data.items():
            if k not in {"id", "created_at", "updated_at"}:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200
