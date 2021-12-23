import pytest
import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def max_book():
    return 12


@pytest.fixture
def club():
    club = {"name": "test club 1", "email": "test1@test.com", "points": "100"}
    return club


@pytest.fixture
def clubs():
    clubs = [
        {"name": "test club 1", "email": "test1@test.com", "points": "100"},
        {"name": "test club 2", "email": "test2@test.com", "points": "20"},
        {"name": "test club 3", "email": "test3@test.com", "points": "30"},
    ]
    return clubs


@pytest.fixture
def competition():
    competition = {
        "name": "test competition 1",
        "date": "2100-12-10 10:00:00",
        "numberOfPlaces": "10",
    }
    return competition


@pytest.fixture
def competitions():
    competitions = [
        {
            "name": "test competition 1",
            "date": "2100-12-10 10:00:00",
            "numberOfPlaces": "10",
        },
        {
            "name": "test competition 2",
            "date": "2020-12-10 10:00:00",
            "numberOfPlaces": "10",
        },
        {
            "name": "test competition 3",
            "date": "2000-12-10 10:00:00",
            "numberOfPlaces": "10",
        },
    ]
    return competitions


@pytest.fixture
def unlisted_club():
    unlisted_club = {
        "name": "test club unlisted",
        "email": "test_unlisted@test.com",
        "points": "100",
    }
    return unlisted_club


@pytest.fixture
def config(mocker, clubs, competitions):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)
