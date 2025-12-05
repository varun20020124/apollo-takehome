import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


# -------------------------------------------------------
# 1. Test database setup (SQLite, file-based for stability)
# -------------------------------------------------------
TEST_DATABASE_URL = "sqlite:///./test_api.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Make sure tables exist in the test DB
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# -------------------------------------------------------
# 2. Override the get_db dependency
# -------------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -------------------------------------------------------
# 3. Sample vehicle payload
# -------------------------------------------------------
sample_vehicle = {
    "vin": "ABC123",
    "manufacturer_name": "Toyota",
    "description": "Sedan",
    "horse_power": 130,
    "model_name": "Corolla",
    "model_year": 2020,
    "purchase_price": 20000.0,
    "fuel_type": "Petrol",
}


# -------------------------------------------------------
# 4. Tests
# -------------------------------------------------------

def test_create_vehicle():
    response = client.post("/vehicle", json=sample_vehicle)
    assert response.status_code == 201

    data = response.json()
    # Depending on your code, VIN might be stored as-is.
    assert data["vin"] == "ABC123"
    assert data["manufacturer_name"] == "Toyota"
    assert data["model_name"] == "Corolla"


def test_duplicate_vehicle():
    # First creation should already be done by test_create_vehicle
    response = client.post("/vehicle", json=sample_vehicle)
    # You likely raise HTTP 400 for duplicate VIN
    assert response.status_code == 400


def test_get_all_vehicles():
    response = client.get("/vehicle")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    # We created one vehicle successfully
    assert len(data) == 1
    assert data[0]["vin"] == "ABC123"


def test_get_vehicle_by_vin():
    response = client.get("/vehicle/ABC123")
    assert response.status_code == 200

    data = response.json()
    assert data["vin"] == "ABC123"
    assert data["model_name"] == "Corolla"


def test_update_vehicle():
    update_payload = {
        "manufacturer_name": "Toyota",
        "description": "Updated Sedan",
        "horse_power": 150,
        "model_name": "Corolla",
        "model_year": 2021,
        "purchase_price": 22000.0,
        "fuel_type": "Hybrid",
    }

    response = client.put("/vehicle/ABC123", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["horse_power"] == 150
    assert data["fuel_type"] == "Hybrid"
    assert data["model_year"] == 2021


def test_delete_vehicle():
    # Delete the vehicle
    response = client.delete("/vehicle/ABC123")
    assert response.status_code == 204

    # Now GET should return 404
    response = client.get("/vehicle/ABC123")
    assert response.status_code == 404