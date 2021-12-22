import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

PLACE_COST = 1
competitions = load_competitions()
clubs = load_clubs()


@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html")


@app.route("/show-summary", methods=["POST"], strict_slashes=False)
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except (IndexError, TypeError):
        return page_not_found()
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>", strict_slashes=False)
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchase-places", methods=["POST"], strict_slashes=False)
def purchase_places():
    compet = [c for c in competitions if c["name"] == request.form["competition_name"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club_name"]][0]
    places_required = int(request.form["places"])
    if places_required > int(club["points"]):
        flash(
            f"You cannot perform this action"
            f"You asked {places_required} place(s), and you have {club['points']} point(s)"
            f"A place costs {PLACE_COST} point(s)"
            f"Therefore you need {places_required * PLACE_COST} point(s) to book {places_required}"
        )
        return render_template("booking.html", club=club, competition=compet)
    elif places_required > int(compet["numberOfPlaces"]):
        flash(
            f"You cannot perform this action"
            f"You asked {places_required} place(s)"
            f"and the competition has {compet['numberOfPlaces']} places left"
        )
        return render_template("booking.html", club=club, competition=compet)
    else:
        flash("Great-booking complete!")
        club["points"] = int(club["points"]) - places_required
        compet["numberOfPlaces"] = int(compet["numberOfPlaces"]) - places_required
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout", strict_slashes=False)
def logout():
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found():
    return render_template("not_found_404.html"), 404
