import pytest
from app import app, quote_premium


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


# ---- unit tests ----
def test_standard_premium():
    assert quote_premium(30, 100000) == 1200.0


@pytest.mark.parametrize("age,expected", [(59, 1200.0), (60, 1800.0)])
def test_senior_loading_boundary(age, expected):
    assert quote_premium(age, 100000) == expected


@pytest.mark.parametrize("age,coverage", [(17, 100000), (30, 0), (30, 999)])
def test_invalid_input_raises(age, coverage):
    with pytest.raises(ValueError):
        quote_premium(age, coverage)


# ---- API tests ----
def test_health(client):
    assert client.get("/health").json == {"status": "ok"}


def test_quote_ok(client):
    r = client.post("/quote", json={"age": 40, "coverage": 50000})
    assert r.status_code == 200
    assert r.json["premium"] == 600.0


def test_quote_missing_field(client):
    r = client.post("/quote", json={"age": 40})
    assert r.status_code == 400