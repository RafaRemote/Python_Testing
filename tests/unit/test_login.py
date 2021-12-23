import pytest


class TestLogin:
    def test_listed_email_should_200(self, client, club, config):
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
    def test_unlisted_mail_should_404(self, client, email, status_code, config):
        """Checks response when unauthenticated user request"""
        response = client.post("/show-summary", data=email, follow_redirects=True)
        assert response.status_code == status_code

    def test_login_bad_request_should_400(
        self, client, mocker, club, clubs, competitions
    ):
        """Checks response when bad request"""
        data = {"address": club["email"]}
        response = client.post("/show-summary", data=data, follow_redirects=True)
        assert response.status_code == 400
