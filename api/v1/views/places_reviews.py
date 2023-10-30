#!/usr/bin/python3
"""API endpoints for review objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET", "POST"], strict_slashes=False
)
def get_reviews(place_id):
    """Get all place reviews, Create review"""
    place = storage.get(cls="Place", id=place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        all_place_reviews = place.reviews
        return jsonify([review.to_dict() for review in all_place_reviews]), 200

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
        elif not data.get("text", None):
            return jsonify({"error": "Missing text"}), 400
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>", methods=["GET", "DELETE", "PUT"],
    strict_slashes=False
)
def get_review(review_id):
    """Get/Delete/Update review by id"""
    review = storage.get(cls="Review", id=review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict()), 200

    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a json"}), 400
        for k, v in data.items():
            if k not in {"id", "created_at", "updated_at"}:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
