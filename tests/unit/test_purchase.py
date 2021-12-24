import random


class TestPurchase:
    def test_should_bad_request_keys_400(self, client, club, competition, config):
        """Checks response when bad request"""
        data = {
            "Klub_name": club["name"],
            "competition_name": competition["name"],
            "places": str(int(club["points"])),
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "bad request" in data

    def test_should_bad_request_values_400(
        self, client, club, competition, competitions, config
    ):
        """Checks response when bad request"""
        data = {
            "club_name": "random",
            "competition_name": "random",
            "places": "random",
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "bad request" in data

    def test_should_bad_request_empty_values_400(
        self, client, club, competition, config
    ):
        """Checks response when bad request"""
        data = {"club_name": "", "competition_name": "", "places": ""}
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "bad request" in data

    def test_should_not_use_more_points_than_have(
        self, client, club, competition, place_cost, config
    ):
        """Checks response when user try to use more points than his club has"""
        data = {
            "club_name": club["name"],
            "competition_name": competition["name"],
            "places": str(int((int(club["points"]) / place_cost)) + 1),
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "CANNOT" in data

    def test_should_deduct_points_from_club(
        self, client, club, competition, place_cost, config
    ):
        """Check club points in response after user book places"""
        places = int(competition["numberOfPlaces"])
        club_points = int(club["points"])
        if places > 0:
            if (club_points) / place_cost > places:
                max = places
            else:
                max = club_points
        places_required = random.choice(range(1, max + 1))
        data = {
            "club_name": club["name"],
            "competition_name": competition["name"],
            "places": str(places_required),
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode("utf-8").split()
        chunk = [i for i in data if "club_points_left" in i][0]
        points_left = int("".join([i for i in chunk if i.isdigit()]))
        assert points_left == club_points - (places_required * place_cost)

    def test_should_not_book_over_limit(
        self, client, club, competition, max_book, config
    ):
        """Check if user can book over a limit (max_book)"""
        data = {
            "club_name": club["name"],
            "competition_name": competition["name"],
            "places": str(max_book + 1),
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "cannot" in data

    def test_should_not_book_negative_places(self, client, club, competition, config):
        """Check if user can book negative number of places"""
        data = {
            "club_name": club["name"],
            "competition_name": competition["name"],
            "places": "-1",
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "cannot" in data

    def test_should_not_book_past_competition(
        self, client, club, past_competition, max_book, config
    ):
        """Check if user can book places for a past competition)"""
        data = {
            "club_name": club["name"],
            "competition_name": past_competition["name"],
            "places": 1,
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode().split()
        assert "cannot" in data
