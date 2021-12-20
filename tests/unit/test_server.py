class TestLogin:
    def test_get_index_should_status_code_200(self, client):
        """Checks index route response when get request"""
        response = client.get("/")
        assert response.status_code == 200

    def test_login_should_status_code_404(self, client, unlistedClub):
        """Checks that unlisted club cannot connect"""
        data = {
            "email": unlistedClub["email"],
        }
        response = client.post("showSummary", data=data)
        assert response.status_code == 404

    def test_login_should_status_code_200(self, client, listedClub):
        """Checks that a listed club can connect"""
        data = {
            "email": listedClub["email"],
        }
        response = client.post("showSummary", data=data)
        assert response.status_code == 200

    def test_login_empty_should_status_code_404(self, client):
        """Checks response with empty input"""
        data = {"email": ""}
        response = client.post("showSummary", data=data)
        assert response.status_code == 404
