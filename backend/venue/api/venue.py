from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from venue.api.schema import VenueSchema
from venue.models import Venue
from website import db
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError


venue_api = Blueprint("venue_api", __name__, url_prefix="/venue")

@venue_api.route("/api", methods=["POST"])
@jwt_required()
@use_args(VenueSchema(), location="json")
def createVenue(args):
    try:
        new_venue = Venue(**args)
        db.session.add(new_venue)
        db.session.commit()
        return jsonify({"success": "Venue created"}), 201
    except IntegrityError:
        return jsonify({"error": "Venue already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@venue_api.route("/api", methods=["GET"])
@jwt_required()
def getVenues():
    venues = Venue.query.all()
    return jsonify(VenueSchema(many=True).dump(venues)), 200

@venue_api.route("/api/<int:venue_id>", methods=["GET"])
@jwt_required()
def getVenue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    if venue == None:
        return jsonify({"error": "Venue not found"}), 404
    return jsonify(VenueSchema().dump(venue)), 200

@venue_api.route("/api/<int:venue_id>", methods=["PUT"])
@jwt_required()
@use_args(VenueSchema(), location="json")
def updateVenue(args, venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    if venue == None:
        return jsonify({"error": "Venue not found"}), 404
    venue.name = args["name"] or venue.name
    venue.place = args["place"] or venue.place
    venue.capacity = args["capacity"] or venue.capacity
    venue.screens = args["screens"] or venue.screens
    db.session.commit()
    return jsonify({"success": "Venue updated"}), 200

@venue_api.route("/api/<int:venue_id>", methods=["DELETE"])
@jwt_required()
def deleteVenue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    if venue == None:
        return jsonify({"error": "Venue not found"}), 404
    db.session.delete(venue)
    db.session.commit()
    return jsonify({"success": "Venue deleted"}), 200   