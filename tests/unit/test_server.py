import random
import pytest


class TestEndpoints:
    @pytest.mark.parametrize("endpoint, status_code", [("/", 200), ("/logout", 200)])
    def test_access_unauthenticated_should_200(self, client, endpoint, status_code):
        """Checks response when unauthenticated user request"""
        response = client.get(endpoint, follow_redirects=True)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "endpoint, status_code", [("/show-summary", 405), ("/purchase-places", 405)]
    )
    def test_access_unauthenticated_user_should_405(
        self, client, endpoint, status_code
    ):
        """Checks response when unauthenticated user request"""
        response = client.get(endpoint, follow_redirects=True)
        assert response.status_code == status_code


class TestLogin:
    def test_login_listed_email_should_200(self, client, club, config):
        """Checks response when authenticated user request"""
        data = {"email": club["email"]}
        response = client.post("/show-summary", data=data, follow_redirects=True)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "email, status_code",
        [
            ({"email": "unlisted@mail.com"}, 404),
            ({"email": ""}, 404),
            ({"email": "$%^"}, 404),
        ],
    )
    def test_login_unlisted_mails_should_404(self, client, email, status_code, config):
        """Checks response when unauthenticated user request"""
        response = client.post("/show-summary", data=email, follow_redirects=True)
        assert response.status_code == status_code

    def test_login_bad_request(self, client, mocker, club, clubs, competitions):
        """Checks response when bad request"""
        data = {"address": club["email"]}
        response = client.post("/show-summary", data=data, follow_redirects=True)
        assert response.status_code == 400


class TestPurchase:
    def test_should_not_use_more_points_than_have(
        self, client, club, competition, config
    ):
        """Checks response when user try to use more points than his club has"""
        data = {
            "club_name": club["name"],
            "competition_name": competition["name"],
            "places": str(int(club["points"]) + 1),
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode()
        assert "cannot" in data

    def test_should_deduct_points_from_club(self, client, club, competition, config):
        """Check club points in response after user book places"""
        places = int(competition["numberOfPlaces"])
        club_points = int(club["points"])
        if places > 0:
            if club_points > places:
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
        data = response.data.decode().split()
        chunk = [i for i in data if "club_points_left" in i][0]
        points_left = int("".join([i for i in chunk if i.isdigit()]))
        assert points_left == club_points - places_required
