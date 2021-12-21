import server
import pytest


class TestLogin:
    def test_login_listed_email_shoudl_200(
        self, client, mocker, club, clubs, competitions
    ):
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
        data = {"email": club["email"]}
        response = client.post("/showSummary", data=data, follow_redirects=True)
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
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
        response = client.post("/showSummary", data=email, follow_redirects=True)
        assert response.status_code == status_code

    def test_login_bad_request(self, client, mocker, club, clubs, competitions):
        mocker.patch.object(server, "clubs", clubs)
        mocker.patch.object(server, "competitions", competitions)
        data = {"address": club["email"]}
        response = client.post("/showSummary", data=data, follow_redirects=True)
        assert response.status_code == 400
