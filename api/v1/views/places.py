#!/usr/bin/python3
"""
Places module
"""


from models.city import City
from models.place import Place
from models.user import User
from models import storage
import json
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_places(city_id):
    """get places by city_id"""
    cities = storage.all(City)
    places = storage.all(Place)
    city_places = []

    for city in cities.values():
        if city.id == city_id:
            for place in places.values():
                if place.city_id == city_id:
                    city_places.append(place.to_dict())
    if city_places is not None:
        return jsonify(city_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_id(place_id):
    """get place_id"""
    places = storage.all(Place)

    for place in places.values():
        if place.id == place_id:
            return jsonify(place.to_dict())

    abort(404)
    return


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place_id(place_id):
    """delete place_id"""
    places = storage.all(Place)

    for place in places.values():
        if place.id == place_id:
            place.delete()
            storage.save()
            return jsonify({}), 200

    abort(404)
    return


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_city_place(city_id):
    """Create place in city"""
    json_dict = request.get_json(silent=True)
    cities = storage.all(City)
    users = storage.all(User)

    if json_dict is None:
        abort(400, "Not a JSON")
    if 'user_id' not in json_dict:
        abort(400, "Missing user_id")
    if 'name' not in json_dict:
        abort(400, "Missing name")

    for city in cities.values():
        if city.id == city_id:
            json_dict['city_id'] = city.id
            for user in users.values():
                if user.id == json_dict['user_id']:
                    new_place = Place(**json_dict)
                    new_place.save()
                    return(jsonify(new_place.to_dict()), 201)
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update place"""
    json_dict = request.get_json(silent=True)
    places = storage.all(Place)
    ignored_keys = ['created_at', 'updated_at', 'id', 'user_id', 'city_id']

    if json_dict is None:
        abort(400, 'Not a JSON')

    for place in places.values():
        if place.id == place_id:
            for k, v in json_dict.items():
                if k not in ignored_keys:
                    setattr(place, k, v)

            place.save()
            return jsonify(place.to_dict()), 200

    abort(404)
