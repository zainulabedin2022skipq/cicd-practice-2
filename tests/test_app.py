import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as c:
        yield c


def test_home_returns_200(client):
    assert client.get("/").status_code == 200


def test_health_reports_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 99),
    (0, 0, 0),
    (10, 90, 100),
])
def test_add_returns_sum(client, a, b, expected):
    assert client.get(f"/api/add/{a}/{b}").get_json()["result"] == expected


def test_add_rejects_non_integer(client):
    assert client.get("/api/add/abc/3").status_code == 404
