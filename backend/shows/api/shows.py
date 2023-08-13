from accounts.models import User
from ticket.models import Ticket
from venue.models import Venue
from website import db
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError
from shows.api.schema import ShowSchema
from flask_jwt_extended import jwt_required
from shows.models import Show
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify


show_api = Blueprint("show_api", __name__, url_prefix="/show")

@show_api.route("/api", methods=["POST"])
@jwt_required()
@use_args(ShowSchema(), location="json")
def createShow(args):
    args['ticket_price'] = args['updated_price']
    try:
        new_show = Show(**args)
        db.session.add(new_show)
        db.session.commit()
        return jsonify({"success": "Show created"}), 201
    except IntegrityError:
        return jsonify({"error": "Show already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@show_api.route("/api", methods=["GET"])
@jwt_required()
def getShows():
    print(User.query.filter_by(id=1).one_or_none())
    shows = Show.query.all()
    shows_response = ShowSchema(many=True).dump(shows)
    final_shows_response = []
    for show in shows_response:
        venue = Venue.query.filter_by(id=show['venue_id']).first()
        tickets_booked_yet = Ticket.query.filter_by(show=show['id']).all()
        total_quantity = 0
        for ticket in tickets_booked_yet:
            total_quantity += ticket.quantity
        show["tickets_available"] = venue.capacity - total_quantity
        final_shows_response.append(show)
    return jsonify(final_shows_response), 200

@show_api.route("/api/<int:show_id>", methods=["GET"])
@jwt_required()
def getShow(show_id):
    show = Show.query.filter_by(id=show_id).first()
    if show == None:
        return jsonify({"error": "Show not found"}), 404
    show = ShowSchema().dump(show)
    venue = Venue.query.filter_by(id=show['venue_id']).first()
    tickets_booked_yet = Ticket.query.filter_by(show=show['id']).all()
    total_quantity = 0
    for ticket in tickets_booked_yet:
        total_quantity += ticket.quantity
    show["tickets_available"] = venue.capacity - total_quantity
    return jsonify(show), 200

@show_api.route("/api/venue", methods=["GET"])
@jwt_required()
def getShowsGroupByVenue():
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

@show_api.route("/api/<int:show_id>", methods=["PUT"])
@jwt_required()
@use_args(ShowSchema(), location="json")
def updateShow(args, show_id):
    show = Show.query.filter_by(id=show_id).first()
    if show == None:
        return jsonify({"error": "Show not found"}), 404
    show.name = args["name"] or show.name
    show.rating = args["rating"] or show.rating
    show.tag = args["tag"] or show.tag
    show.updated_price = args["updated_price"] or show.updated_price
    show.venue_id = args["venue_id"] or show.venue_id
    show.date = args["date"] or show.date
    db.session.commit()
    return jsonify({"success": "Show updated"}), 200

@show_api.route("/api/<int:show_id>", methods=["DELETE"])
@jwt_required()
def deleteShow(show_id):
    show = Show.query.filter_by(id=show_id).first()
    if show == None:
        return jsonify({"error": "Show not found"}), 404
    db.session.delete(show)
    db.session.commit()
    return jsonify({"success": "Show deleted"}), 200