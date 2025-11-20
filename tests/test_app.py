import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity():
    activity_name = "Chess Club"
    email = "test@student.com"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_for_nonexistent_activity():
    activity_name = "Nonexistent Club"
    email = "test@student.com"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant():
    activity_name = "Chess Club"
    email = "test@student.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # Ensure the participant is registered
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Successfully removed {email} from {activity_name}"


def test_unregister_nonexistent_participant():
    activity_name = "Chess Club"
    email = "nonexistent@student.com"
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"