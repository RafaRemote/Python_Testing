from locust import HttpUser, task

# CLI, without webinterface, for a result in the terminal
# with parameters:
# - f: file
# - H: host
# - r: spawn_rate
# - u: users
# - headless: disable the webinterface
# - autostart: start the test immediately (without disabling the webinterface)
# command below:
# locust -f locustfile.py -H http://127.0.0.1:5000/ -u 6 -r 1 --headless
#  or
# locust -f locustfile.py -H http://127.0.0.1:5000/ -u 6 -r 1 --autostart


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        data = {"email": "admin@irontemple.com"}
        self.client.post("/show-summary", data=data)

    @task
    def book(self):
        self.client.get("/book/Future%20Competition/Iron%20Temple")

    @task
    def purchasePlaces(self):
        data = {"club": "Iron Temple", "competition": "Future Competition", "places": 1}
        self.client.post("/purchase-places", data=data)

    @task
    def clubsPoints(self):
        self.client.get("/points-board")

    @task
    def logout(self):
        self.client.get("/logout")
