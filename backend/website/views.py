from flask import Blueprint, request, render_template, redirect, url_for
from shows.models import Show
from flask_login import login_user, login_required, logout_user, current_user
from venue.models import Venue

views = Blueprint("views", __name__, url_prefix="/")


@views.route("/")
def home():  
    shows = Show.query.all()
    return render_template("home.html", shows=shows, user=current_user)

@views.route("search/", methods=["POST"])
def search():
    search = request.form.get("search")
    print(search)
    if search:
        shows = Show.query.filter(Show.name.contains(search)).all()
        venues = Venue.query.filter(Venue.name.contains(search)).all()
        print(shows)
        search_results = {
            "shows": shows,
            "venues": venues
        }
        return render_template("search.html", user=current_user, **search_results)
    else:
        shows = Show.query.all()
        return render_template("home.html", shows=shows, user=current_user)