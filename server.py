import json
import requests
import datetime as dt
import time
from flask import Flask, render_template, request, redirect, flash, url_for

MAX_BOOK = 12
PLACE_COST = 3


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        for i in list_of_competitions:
            i["date_stamp"] = dt.datetime.timestamp(
                dt.datetime.strptime(i["date"], "%Y-%m-%d %H:%M:%S")
            )
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()
now = time.time()


@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html", clubs=clubs)


@app.route("/show-summary", methods=["GET", "POST"], strict_slashes=False)
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except (IndexError, TypeError):
        return page_not_found()
    except requests.exceptions.RequestException:
        flash("Something went wrong-please try again")
        return redirect(url_for(index))
    return render_template(
        "welcome.html",
        now=now,
        club=club,
        competitions=competitions,
        place_cost=PLACE_COST,
    )


@app.route("/book/<competition>/<club>", strict_slashes=False)
def book(club, competition):
    if club and competition:
        try:
            club = [i for i in clubs if i["name"] == club][0]
            competition = [c for c in competitions if c["name"] == competition][0]
        except IndexError:
            flash("Something went wrong-please try again")
            return render_template("index.html")
        try:
            club["points"] > 0
        except TypeError:
            club = [i for i in clubs if i["name"] == club["name"]][0]
            competition = [c for c in competitions if c["name"] == competition["name"]][
                0
            ]
        if int(club["points"]) < 0:
            flash("Something went wrong-please try again")
            return render_template(
                "welcome.html",
                now=now,
                club=club,
                competitions=competitions,
                place_cost=PLACE_COST,
            )
        elif int(club["points"]) > 0:
            if (
                int(club["points"]) / PLACE_COST >= MAX_BOOK
                and competition["numberOfPlaces"] >= MAX_BOOK
            ):
                flash(f"max places you can book is {MAX_BOOK}")
                return render_template(
                    "booking.html",
                    club=club,
                    competition=competition,
                    maxi=MAX_BOOK,
                )
            elif (int(club["points"]) / PLACE_COST) >= int(
                competition["numberOfPlaces"]
            ):
                flash(f"max places you can book is {competition['numberOfPlaces']}")
                return render_template(
                    "booking.html",
                    club=club,
                    competition=competition,
                    maxi=int(competition["numberOfPlaces"] / PLACE_COST),
                )
            else:
                flash(
                    f'max places you can book is {int(int(club["points"]) / PLACE_COST)}'
                )
                return render_template(
                    "booking.html",
                    club=club,
                    competition=competition,
                    maxi=int(int(club["points"]) / PLACE_COST),
                )
        else:
            flash("You cannot access booking page, you have no points left")
            return render_template(
                "welcome.html",
                now=now,
                club=club,
                competitions=competitions,
                place_cost=PLACE_COST,
            )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html",
            now=now,
            club=club,
            competitions=competitions,
            place_cost=PLACE_COST,
        )


@app.route("/purchase-places", methods=["POST"], strict_slashes=False)
def purchase_places():
    try:
        request.form["club_name"] and request.form["competition_name"] and request.form[
            "places"
        ]
    except Exception:
        flash("bad request")
        return render_template("index.html")
    try:
        compet = [
            c for c in competitions if c["name"] == request.form["competition_name"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club_name"]][0]
        places = request.form["places"]
        if compet["date_stamp"] < now:
            flash("You cannot purchase places for a past competition")
            return render_template(
                "booking.html",
                club=club,
                competition=compet,
                maxi=MAX_BOOK,
            )
    except Exception:
        flash("bad request")
        return render_template("index.html")
    if places.startswith("-") and club["points"][1:].isdigit():
        flash("you cannot book a negative number of places")
        return render_template(
            "booking.html",
            club=club,
            competition=compet,
            maxi=MAX_BOOK,
        )
    else:
        places_required = int(request.form["places"])
    if (places_required * PLACE_COST) > int(club["points"]):
        flash("You cannot perform this action")
        return render_template(
            "welcome.html",
            now=now,
            club=club,
            competitions=competitions,
            place_cost=PLACE_COST,
        )
    elif places_required > int(compet["numberOfPlaces"]):
        flash(
            f"You cannot perform this action"
            f"You asked {places_required} place(s)"
            f"and the competition has {compet['numberOfPlaces']} places left"
        )
        return render_template("booking.html", club=club, competition=compet)
    else:
        flash("Great-booking complete!")
        club["info"] = [
            ["Places Booked", places_required],
            ["Cost Per Place", PLACE_COST],
            ["Points Redeemed", places_required * PLACE_COST],
            ["Club Points Before", club["points"]],
            ["Club Points After", int(club["points"]) - (places_required * PLACE_COST)],
        ]
        club["points"] = int(club["points"]) - (places_required * PLACE_COST)
        compet["numberOfPlaces"] = int(compet["numberOfPlaces"]) - places_required
        return render_template(
            "welcome.html",
            now=now,
            club=club,
            competitions=competitions,
            place_cost=PLACE_COST,
        )


# TODO: Add route for points display


@app.route("/points-board", strict_slashes=False)
def points_board():
    return render_template("points_board.html", clubs=clubs)


@app.route("/logout", strict_slashes=False)
def logout():
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found():
    return render_template("not_found_404.html"), 404
