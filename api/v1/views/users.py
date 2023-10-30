#!/usr/bin/python3
"""API endpoints for user objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def get_users():
    """Get all users"""
    if request.method == "GET":
        all_users = storage.all(cls="User")
        return (
            jsonify([user.to_dict() for user_id, user in all_users.items()]),
            200,
        )

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        elif not data.get("email", None):
            return jsonify({"error": "Missing email"}), 400
        elif not data.get("password", None):
            return jsonify({"error": "Missing password"}), 400
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def get_user(user_id):
    """Get/Delete user by id"""
    user = storage.get(cls="User", id=user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        for k, v in data.items():
            if k not in {"id", "created_at", "updated_at"}:
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
