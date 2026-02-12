import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to static index.html
    assert "text/html" in response.headers.get("content-type", "")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Art Studio/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu for Art Studio" in response.json().get("message", "")

def test_signup_for_activity_already_signed_up():
    # Sign up first
    client.post("/activities/Drama Club/signup?email=repeat@mergington.edu")
    # Try again
    response = client.post("/activities/Drama Club/signup?email=repeat@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # Sign up first
    client.post("/activities/Science Club/signup?email=remove@mergington.edu")
    response = client.delete("/activities/Science Club/unregister?email=remove@mergington.edu")
    assert response.status_code == 200
    assert "Removed remove@mergington.edu from Science Club" in response.json().get("message", "")

def test_unregister_from_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_participant_not_found():
    response = client.delete("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
