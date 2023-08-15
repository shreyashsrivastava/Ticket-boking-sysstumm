from shows.api.schema import ShowSchema
from ticket.models import Ticket
from shows.models import Show
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from venue.api.schema import VenueSchema, SearchSchema
from venue.models import Venue
from website import db
from webargs.flaskparser import use_args
from sqlalchemy import or_
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

@venue_api.route("/api/generate_csv/<int:venue_id>", methods=["POST"])
@jwt_required()
def downloadCSV(venue_id):
    from tasks.tasks import generate_csv_task
    
    generate_csv_task.delay(venue_id)
    return jsonify({"success": "Request submitted, you will receive an email shortly!"}), 200

@venue_api.route("/api/search", methods=["POST"])
@jwt_required()
@use_args(SearchSchema(), location="json")
def api_search(args):
    search_term = args['search']
    print(search_term)
    if search_term:
        venues = Venue.query.filter(or_(Venue.name.ilike(f'%{search_term}%'), Venue.place.ilike(f'%{search_term}%'))).all()

        shows = Show.query.filter(or_(Show.name.ilike(f'%{search_term}%'), Show.tag.ilike(f'%{search_term}%'))).all()

        final_response = []

        for venue in venues:
            venue_shows = [show for show in shows if show.venue_id == venue.id]
            shows_response = ShowSchema(many=True).dump(venue_shows)
            final_shows_response = []

            for show in shows_response:
                tickets_booked_yet = Ticket.query.filter_by(show=show['id']).all()
                total_quantity = sum(ticket.quantity for ticket in tickets_booked_yet)
                show["tickets_available"] = venue.capacity - total_quantity
                final_shows_response.append(show)

            final_response.append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "shows": final_shows_response
            })

        return jsonify(final_response), 200
    else:
        venues = Venue.query.all()
        final_response = []
        for venue in venues:
            shows = Show.query.filter_by(venue_id=venue.id).all()
            shows_response = ShowSchema(many=True).dump(shows)
            final_shows_response = []
            for show in shows_response:
                tickets_booked_yet = Ticket.query.filter_by(show=show['id']).all()
                total_quantity = 0
                for ticket in tickets_booked_yet:
                    total_quantity += ticket.quantity
                show["tickets_available"] = venue.capacity - total_quantity
                final_shows_response.append(show)
            final_response.append({"venue_id": venue.id, "venue_name": venue.name, "shows": final_shows_response})
        return jsonify(final_response), 200