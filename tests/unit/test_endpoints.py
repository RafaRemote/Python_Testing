import pytest


class TestEndpoints:
    @pytest.mark.parametrize("endpoint, status_code", [("/", 200), ("/logout", 200)])
    def test_index_logout_unauthenticated_user_should_200(
        self, client, endpoint, status_code
    ):
        """Checks response when getting index and logout endpoints"""
        response = client.get(endpoint, follow_redirects=True)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "endpoint, status_code", [("/show-summary", 400), ("/purchase-places", 405)]
    )
    def test_summary_and_purchase_unauthenticated_user_should_fail(
        self, client, endpoint, status_code
    ):
        """Checks response when unauthenticated user request"""
        response = client.get(endpoint, follow_redirects=True)
        assert response.status_code == status_code

    def test_book_authenticated_user_should_200(
        self, client, club, competition, config
    ):
        club_name = club["name"].replace(" ", "%20")
        competition_name = competition["name"].replace(" ", "%20")
        response = client.get(
            f"/book/{club_name}/{competition_name}", follow_redirects=True
        )
        assert response.status_code == 200

    def test_book_unauthenticated_user_should_get_wrong(
        self, client, competition, config
    ):
        club_name = "random"
        competition_name = competition["name"].replace(" ", "%20")
        response = client.get(
            f"/book/{club_name}/{competition_name}", follow_redirects=True
        )
        assert "wrong" in response.data.decode()
