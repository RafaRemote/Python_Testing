class TestClass:
    def test_should_get_index_and_get_welcome_page(self, client, club, config):
        """User access to index page, connects and gets to welcome page"""
        client.get("/")
        data = {"email": club["email"]}
        response = client.post("/show-summary", data=data)
        assert response.status_code == 200

    def test_should_get_index_and_get_club_points(self, client, club, config):
        """
        User access to index page
        gets to clubs points board page
        logout and therefore comes back to index
        connects with his email
        """
        client.get("/")
        client.get("/points-board")
        client.get("/logout")
        data = {"email": club["email"]}
        response = client.post("/show-summary", data=data)
        assert response.status_code == 200

    def test_should_book_places_two_times(self, client, club, competition, config):
        """
        User book 1 place for a competition
        access again to the booking page for the same competition
        user book again 1 place for the same competition
        """
        data = {"club": club["name"], "competition": competition["name"], "places": 1}
        client.post("/purchase-places", data=data)
        client.get(f"/book/{competition['name']}/{club['name']}")
        response = client.post("/purchase-places", data=data)
        assert response.status_code == 200
