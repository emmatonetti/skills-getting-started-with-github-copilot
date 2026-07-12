from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_participant_removes_email_from_activity():
    with TestClient(app) as client:
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        assert email in activities[activity_name]["participants"]

        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
