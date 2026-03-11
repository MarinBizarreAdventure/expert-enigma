import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PROFILE_PAYLOAD = {
    "user_id": "test-user-001",
    "name": "Test User",
    "default_city": "Chisinau",
    "style_preferences": ["casual"],
    "budget_default": "medium",
    "dietary_restrictions": [],
    "favorite_cuisines": [],
    "avoid": [],
}


@pytest.fixture(autouse=True)
def clean_users_json():
    path = Path("data/users.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text("{}")
    yield
    path.write_text("{}")


def test_create_profile():
    r = client.post("/api/v1/profile", json=PROFILE_PAYLOAD)
    assert r.status_code == 201
    body = r.json()
    assert body["user_id"] == "test-user-001"
    assert body["name"] == "Test User"


def test_create_profile_duplicate():
    client.post("/api/v1/profile", json=PROFILE_PAYLOAD)
    r = client.post("/api/v1/profile", json=PROFILE_PAYLOAD)
    assert r.status_code == 409


def test_get_profile():
    client.post("/api/v1/profile", json=PROFILE_PAYLOAD)
    r = client.get("/api/v1/profile/test-user-001")
    assert r.status_code == 200
    assert r.json()["user_id"] == "test-user-001"


def test_get_profile_not_found():
    r = client.get("/api/v1/profile/nonexistent")
    assert r.status_code == 404


def test_update_profile():
    client.post("/api/v1/profile", json=PROFILE_PAYLOAD)
    r = client.patch(
        "/api/v1/profile/test-user-001",
        json={"style_preferences": ["streetwear", "smart casual"]},
    )
    assert r.status_code == 200
    assert "streetwear" in r.json()["style_preferences"]
