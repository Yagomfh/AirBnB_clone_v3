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
            return jsonify(city_places)

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
            json_dict['city_id'] = city_id
            for user in users.values():
                if user.id == json_dict['user_id']:
                    new_place = Place(**json_dict)
                    new_place.save()
                    return jsonify(new_place.to_dict()), 201
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


@app_views.route('places_search',
                 methods=['POST'], strict_slashes=False)
def retrieve_place_json():
    """Endpoint that retrieves all Place objects
    depending of the JSON in the body of the reques"""
    data = request.json
    places = storage.all(Place)
    response = []
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if data != {} and ('states' in data or 'cities' in data):
        print("in")
        if 'state' in data and data['states'] == []:
            if 'cities' in data and data['cities'] == []:
                response = [place for place in places.values()]
        if 'states' in data:
            for state_id in data['states']:
                state = storage.get(State, state_id)
                for city in state.cities:
                    for place in city.places:
                        response.append(place)
        if 'cities' in data:
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                for place in city.places:
                    response.append(place)
    else:
        response = [place for place in places.values()]
    if 'amenities' in data:
        response_copy = response.copy()
        for place in response_copy:
            for amenity_id in data['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                if amenity not in place.amenities:
                    response.remove(place)
                    break
    return jsonify([place.to_dict() for place in response])
