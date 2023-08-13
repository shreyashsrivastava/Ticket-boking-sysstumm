from shows.models import Show
from ticket.api.schema import TicketSchema
from flask_jwt_extended import jwt_required
from ticket.models import Ticket
from venue.models import Venue
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import current_user
from flask import Blueprint, jsonify
from website import db

ticket_api = Blueprint("ticket_api", __name__, url_prefix="/ticket")

@ticket_api.route("/api", methods=["POST"])
@jwt_required()
@use_args(TicketSchema(), location="json")
def createTicket(args):
    args['user'] = current_user.id
    try:
        new_ticket = Ticket(**args)
        db.session.add(new_ticket)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Systumm error"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    show = Show.query.filter_by(id=args["show"]).first()
    venue = Venue.query.filter_by(id=show.venue_id).first()
    tickets_booked_yet = Ticket.query.filter_by(show=args["show"]).all()
    total_quantity = 0
    for ticket in tickets_booked_yet:
        total_quantity += ticket.quantity
    if total_quantity + args["quantity"] > venue.capacity:
        return jsonify({"error": "Tickets not available"}), 400
    
    # dynamically increased the ticket price based on the tickets booked but not more than the 100% of the original price
    percentage = total_quantity / venue.capacity
    price = show.updated_price + show.updated_price * percentage
    if price > show.ticket_price * 2:
        price = show.ticket_price * 2
    show.updated_price = price
    db.session.commit()
    
    return jsonify({"success": "Ticket created"}), 201
    
    
    
@ticket_api.route("/api", methods=["GET"])
@jwt_required()
def getTickets():
    tickets = Ticket.query.filter_by(user=current_user.id).all()
    resp = TicketSchema(many=True).dump(tickets)
    final_resp = []
    # send name of the show and venue in the response
    for ticket in resp:
        show = Show.query.filter_by(id=ticket['show']).first()
        venue = Venue.query.filter_by(id=show.venue_id).first()
        ticket['show_name'] = show.name
        ticket['venue_name'] = venue.name
        final_resp.append(ticket)
    return jsonify(final_resp), 200

@ticket_api.route("/api/<int:ticket_id>", methods=["GET"])
@jwt_required()
def getTicket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id, user=current_user.id).first()
    if ticket == None:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(TicketSchema().dump(ticket)), 200

@ticket_api.route("/api/<int:ticket_id>", methods=["PUT"])
@jwt_required()
@use_args(TicketSchema(), location="json")
def updateTicket(args, ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if ticket == None:
        return jsonify({"error": "Ticket not found"}), 404
    ticket.date = args["date"] or ticket.date
    ticket.show = args["show"] or ticket.show
    ticket.quantity = args["quantity"] or ticket.quantity
    db.session.commit()
    return jsonify({"success": "Ticket updated"}), 200

@ticket_api.route("/api/<int:ticket_id>", methods=["DELETE"])
@jwt_required()
def deleteTicket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if ticket == None:
        return jsonify({"error": "Ticket not found"}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"success": "Ticket deleted"}), 200