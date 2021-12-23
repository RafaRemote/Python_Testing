import pytest
import server
import datetime as dt


@pytest.fixture
def next_year():
    next_year = str(int(dt.datetime.now().strftime("%Y")) + 1)
    return next_year


@pytest.fixture
def last_year():
    last_year = str(int(dt.datetime.now().strftime("%Y")) - 1)
    return last_year


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def max_book():
    return 12


@pytest.fixture
def clubs():
    clubs = [
        {"name": "test club 1", "email": "test1@test.com", "points": "100"},
        {"name": "test club 2", "email": "test2@test.com", "points": "20"},
        {"name": "test club 3", "email": "test3@test.com", "points": "30"},
    ]
    return clubs


@pytest.fixture
def club(clubs):
    return clubs[0]


@pytest.fixture
def competitions(last_year, next_year):
    date_next_year = dt.datetime.now().strftime(f"%{next_year}-%m-%d %H:%M:%S")
    date_last_year = dt.datetime.now().strftime(f"%{last_year}-%m-%d %H:%M:%S")
    competitions = [
        {
            "name": "test competition 1",
            "date": date_next_year,
            "date_stamp": dt.datetime.timestamp(
                dt.datetime.strptime(date_next_year, "%Y-%m-%d %H:%M:%S")
            ),
            "numberOfPlaces": "10",
        },
        {
            "name": "test competition 2",
            "date": date_last_year,
            "date_stamp": dt.datetime.timestamp(
                dt.datetime.strptime(date_last_year, "%Y-%m-%d %H:%M:%S")
            ),
            "numberOfPlaces": "10",
        },
        {
            "name": "test competition 3",
            "date": date_last_year,
            "date_stamp": dt.datetime.timestamp(
                dt.datetime.strptime(date_last_year, "%Y-%m-%d %H:%M:%S")
            ),
            "numberOfPlaces": "10",
        },
    ]
    return competitions


@pytest.fixture
def competition(competitions):
    return competitions[0]


@pytest.fixture
def past_competition(competitions):
    return competitions[1]


@pytest.fixture
def config(mocker, clubs, competitions):
    mocker.patch.object(server, "clubs", clubs)
    mocker.patch.object(server, "competitions", competitions)
