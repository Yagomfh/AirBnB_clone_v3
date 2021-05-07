#!/usr/bin/python3
"""Module for index file"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """States endpoint to retrieve all states"""
    all_objs = storage.all(State)
    response = []
    for obj in all_objs.values():
        response.append(obj.to_dict())
    return jsonify(response)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Endpoint return a state object"""
    all_objs = storage.all(State)
    for obj in all_objs.values():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Endpoint to delete a state object"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Endpoint to post a state object"""
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(name=request.json['name'])
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Endpoint to put a state object"""
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if state:
        state.name = request.json['name']
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
    abort(404)
