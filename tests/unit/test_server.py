import random
import server
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
    def test_login_listed_email_should_200(
        self, client, mocker, club, clubs, competitions
    ):
        """Checks response when authenticated user request"""
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
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
    def test_login_unlisted_mails_should_404(
        self, client, mocker, email, status_code, clubs, competitions
    ):
        """Checks response when unauthenticated user request"""
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
        response = client.post("/show-summary", data=email, follow_redirects=True)
        assert response.status_code == status_code

    def test_login_bad_request(self, client, mocker, club, clubs, competitions):
        """Checks response when bad request"""
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
        data = {"address": club["email"]}
        response = client.post("/show-summary", data=data, follow_redirects=True)
        assert response.status_code == 400


class TestPurchase:
    def test_should_not_use_more_points_than_have(
        self, client, mocker, club, competition, clubs, competitions
    ):
        """Checks response when user try to use more points than his club has"""
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
        places = int(competition["numberOfPlaces"]) + 1
        data = {
            "club_name": club["name"],
            "competition_name": competition["name"],
            "places": str(places),
        }
        response = client.post("/purchase-places", data=data, follow_redirects=True)
        data = response.data.decode("utf-8").split()
        assert "cannot" in data

    def test_should_deduct_points_from_club(
        self, client, mocker, club, competition, clubs, competitions
    ):
        """Check club points in response after user book places"""
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
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
        data = response.data.decode("utf-8").split()
        club_points_left = int(data[(data.index("Available:") + 1)])
        assert club_points_left == club_points - places_required
