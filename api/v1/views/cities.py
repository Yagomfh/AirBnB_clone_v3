#!/usr/bin/python3
"""Module for index file"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False)
def get_cities_from_state(state_id):
    """Endpoint to get all city objects from a state"""
    state = storage.get(State, state_id)
    if state is not None:
        response = []
        for city in state.cities:
            response.append(city.to_dict())
        return jsonify(response)
    abort(404)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False)
def get_city(city_id):
    """Endpoint to get a city object"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Endpoint to delete a city object"""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """Endpoint to post a city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def put_city(city_id):
    """Endpoint to put a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city.name = request.json['name']
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
