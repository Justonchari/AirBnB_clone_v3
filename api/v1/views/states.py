#!/usr/bin/python3
"""API endpoints for state objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def get_states():
    """Get all states"""
    if request.method == "GET":
        all_states = storage.all(cls="State")
        return (
            jsonify([state.to_dict() for state_id,
                     state in all_states.items()]),
            200,
        )

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        if not data.get("name", None):
            return jsonify({"error": "Missing name"}), 400
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def get_state(state_id):
    """Get/Delete state by id"""
    state = storage.get(cls="State", id=state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        for k, v in data.items():
            if k not in {"id", "created_at", "updated_at"}:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200
