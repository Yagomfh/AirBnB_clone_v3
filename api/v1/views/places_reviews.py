#!/usr/bin/python3
"""
Methods for Review class in our API
"""
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
import json
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_review(place_id):
    """get review by place"""
    places = storage.all(Place)
    reviews = storage.all(Review)
    all_reviews = []

    for place in places.values():
        if place.id == place_id:
            for review in reviews.values():
                if review.place_id == place_id:
                    all_reviews.append(review.to_dict())
                    return jsonify(all_reviews)

    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get a selected review"""
    reviews = storage.all(Review)

    for review in reviews.values():
        if review.id == review_id:
            return(jsonify(review.to_dict()))

    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review"""
    reviews = storage.all(Review)

    for review in reviews.values():
        if review.id == review_id:
            review.delete()
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """creates a review"""
    json_dict = request.get_json(silent=True)
    places = storage.all(Place)

    if json_dict is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_dict:
        abort(400, 'Missing user_id')
    if 'text' not in json_dict:
        abort(400, 'Missing text')

    for place in places.values():
        if place.id == place_id:
            json_dict["place_id"] = place_id

            user = storage.get(User, json_dict["user_id"])

            if user is not None:
                new_review = Review(**json_dict)
                new_review.save()
                return jsonify(new_review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    json_dict = request.get_json(silent=True)
    reviews = storage.all(Review)
    ignored_keys = ['created_at', 'updated_at', 'id', 'user_id', 'place_id']

    if json_dict is None:
        abort(400, 'Not a JSON')

    for review in reviews.values():
        if review.id == review_id:
            for k, v in json_dict.items():
                if k not in ignored_keys:
                    setattr(review, k, v)

            review.save()
            return jsonify(review.to_dict()), 200

    abort(404)
