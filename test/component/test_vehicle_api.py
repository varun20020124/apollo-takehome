"""
1. Use FastAPI’s TestClient to test the actual API endpoints.
2. Override the DB dependency so tests run with a temporary DB.
3. Validate:
Full request → response cycle
Error handling (400, 404, 422)
JSON validation
Duplicate VIN logic
Success paths and failure paths
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# -----------------------------
# Test DB setup (file-based)
# -----------------------------
TEST_DB_URL = "sqlite:///./test_component.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# -----------------------------
# Sample payloads
# -----------------------------
vehicle_payload = {
    "vin": "ABC123",
    "manufacturer_name": "Toyota",
    "description": "Sedan",
    "horse_power": 130,
    "model_name": "Corolla",
    "model_year": 2020,
    "purchase_price": 20000.00,
    "fuel_type": "Petrol",
}

update_payload = {
    "manufacturer_name": "Toyota",
    "description": "Updated Sedan",
    "horse_power": 150,
    "model_name": "Corolla",
    "model_year": 2021,
    "purchase_price": 22000.00,
    "fuel_type": "Hybrid",
}


# ---------------------------------------------------
# POST /vehicle
# ---------------------------------------------------

def test_create_vehicle():
    """
    Tests that a new vehicle can be successfully created.
    Verifies:
      - API returns HTTP 201
      - Response contains correct VIN
    """
    r = client.post("/vehicle", json=vehicle_payload)
    assert r.status_code == 201
    assert r.json()["vin"] == "ABC123"


def test_duplicate_vehicle():
    """
    Tests that creating a vehicle with an existing VIN
    returns HTTP 400 instead of inserting a duplicate record.
    """
    r = client.post("/vehicle", json=vehicle_payload)
    assert r.status_code == 400


# ---------------------------------------------------
# GET /vehicle
# ---------------------------------------------------

def test_get_all_vehicles():
    """
    Tests returning all vehicles.
    Verifies:
      - API returns HTTP 200
      - Exactly one vehicle exists in DB
      - VIN matches expected value
    """
    r = client.get("/vehicle")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["vin"] == "ABC123"


def test_get_vehicle_success():
    """
    Tests retrieving a vehicle by VIN.
    Verifies:
      - API returns HTTP 200
      - Response body contains the correct VIN
    """
    r = client.get("/vehicle/ABC123")
    assert r.status_code == 200
    assert r.json()["vin"] == "ABC123"


def test_get_vehicle_not_found():
    """
    Tests retrieving a non-existent VIN.
    API should return HTTP 404.
    """
    r = client.get("/vehicle/DOESNOTEXIST")
    assert r.status_code == 404


# ---------------------------------------------------
# PUT /vehicle/{vin}
# ---------------------------------------------------

def test_update_vehicle_success():
    """
    Tests updating an existing vehicle.
    Verifies:
      - API returns HTTP 200
      - Updated fields reflect the new values
    """
    r = client.put("/vehicle/ABC123", json=update_payload)
    assert r.status_code == 200
    assert r.json()["horse_power"] == 150


def test_update_vehicle_not_found():
    """
    Tests updating a vehicle that does not exist.
    API should return HTTP 404.
    """
    r = client.put("/vehicle/NOPE", json=update_payload)
    assert r.status_code == 404


# ---------------------------------------------------
# DELETE /vehicle/{vin}
# ---------------------------------------------------

def test_delete_vehicle_success():
    """
    Tests deleting an existing vehicle.
    Verifies:
      - API returns HTTP 204 (no content)
    """
    r = client.delete("/vehicle/ABC123")
    assert r.status_code == 204


def test_delete_vehicle_not_found():
    """
    Tests deleting a vehicle that no longer exists.
    API should return HTTP 404.
    """
    r = client.delete("/vehicle/ABC123")
    assert r.status_code == 404


# ---------------------------------------------------
# Validation & Error Handling Tests
# ---------------------------------------------------

def test_invalid_json_returns_400():
    """
    Ensure malformed JSON fails validation before reaching the endpoint.
    FastAPI raises a RequestValidationError → returns 422 Unprocessable Entity.
    """
    bad_payload = "{ invalid json }"

    response = client.post(
        "/vehicle",
        data=bad_payload,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422



def test_invalid_json_returns_422():
    """
    Ensure that malformed JSON returns a 422 Unprocessable Entity error.
    FastAPI validates JSON parsing before hitting the endpoint handler,
    so invalid JSON bodies never produce a 400 at application level.
    """
    bad_payload = "{ invalid json }"  # malformed JSON string

    response = client.post(
        "/vehicle",
        data=bad_payload,  # raw body, not JSON
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422