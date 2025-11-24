import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Signup
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 400)  # 400 if already signed up
    # Unregister
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 404)  # 404 if not found

def test_signup_twice():
    email = "twice@mergington.edu"
    activity = "Programming Class"
    # First signup
    client.delete(f"/activities/{activity}/signup?email={email}")
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json().get("detail", "")
    # Cleanup
    client.delete(f"/activities/{activity}/signup?email={email}")
