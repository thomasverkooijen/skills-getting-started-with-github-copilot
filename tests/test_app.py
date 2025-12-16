import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities():
    # Deep copy and restore around each test to keep tests isolated
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(orig)


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_presence():
    email = "testuser1@mergington.edu"
    activity = "Chess Club"

    # Ensure not present
    assert email not in activities[activity]["participants"]

    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Check participant added
    res2 = client.get("/activities")
    data = res2.json()
    assert email in data[activity]["participants"]


def test_double_signup_fails_across_activities():
    email = "testuser2@mergington.edu"
    # Sign up for Programming Class
    res = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert res.status_code == 200

    # Attempt to sign up for Chess Club should fail (app prevents signing up for multiple activities)
    res2 = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert res2.status_code == 400
    assert "Student already signed up" in res2.json().get("detail", "")


def test_remove_participant():
    # Ensure a known participant exists
    activity = "Tennis Club"
    email = activities[activity]["participants"][0]

    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert f"Removed {email}" in res.json().get("message", "")

    # Verify removed
    res2 = client.get("/activities")
    data = res2.json()
    assert email not in data[activity]["participants"]
