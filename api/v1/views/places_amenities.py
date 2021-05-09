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
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    return jsonify([amnty.to_dict() for amnty in amenities])


@app_views.route('places/<string:place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenities(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            place.save()
        else:
            abort(404)
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
            place.save()
        else:
            abort(404)
    return jsonify({})


@app_views.route('places/<string:place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenities(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
        else:
            return jsonify(amenity.to_dict()), 200
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            storage.save()
        else:
            return jsonify(amenity.to_dict()), 200
    return jsonify(amenity.to_dict()), 201
