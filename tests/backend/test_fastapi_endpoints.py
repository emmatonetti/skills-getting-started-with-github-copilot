from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(original_state))


def test_root_redirects_to_static_index():
    # Arrange
    with TestClient(app) as client:
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_catalog():
    # Arrange
    with TestClient(app) as client:
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        payload = response.json()
        assert "Chess Club" in payload
        assert payload["Chess Club"]["participants"][0] == "michael@mergington.edu"


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    with TestClient(app) as client:
        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_returns_404_for_unknown_activity():
    # Arrange
    with TestClient(app) as client:
        # Act
        response = client.post(
            "/activities/Unknown Activity/signup",
            params={"email": "student@mergington.edu"},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
