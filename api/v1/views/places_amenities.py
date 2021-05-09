#!/usr/bin/python3
"""Module for index file"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from os import getenv


@app_views.route('places/<string:place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            response = [amnty.to_dict() for amnty in place.amenities]
        else:
            response = []
            for amenity_id in place.amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                response.append(amenity.to_dict())
        return jsonify(response)
    abort(404)


@app_views.route('places/<string:place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenities(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                amenity.delete()
                storage.save()
            else:
                abort(404)
        else:
            if amenity_id in place.amenity_ids:
                amenity.delete()
                storage.save()
            else:
                abort(404)
        return jsonify({})
    abort(404)


@app_views.route('places/<string:place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenities(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity not in place.amenities:
                place.amenities.append(amenity)
                storage.save()
            else:
                return jsonify(amenity.to_dict())
        else:
            if amenity_id not in place.amenity_ids:
                place.amenity_ids.append(amenity_id)
                storage.save()
            else:
                return jsonify(amenity.to_dict())
        return jsonify(amenity.to_dict()), 201
    abort(404)
