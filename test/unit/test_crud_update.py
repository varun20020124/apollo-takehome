from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

# ---------------------------------------------------------------------
# Use a separate SQLite database file for update unit tests
# ---------------------------------------------------------------------
engine = create_engine("sqlite:///./unit_update.db", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine)

# Reset database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------
# Helper to insert a sample vehicle
# ---------------------------------------------------------------------
def setup_sample():
    db = TestingSession()
    repo = crud.VehicleRepository(db)

    payload = schemas.VehicleCreate(
        vin="UPD1",
        manufacturer_name="Audi",
        description="Sport",
        horse_power=250,
        model_name="A4",
        model_year=2020,
        purchase_price=30000.0,
        fuel_type="Petrol"
    )

    repo.create(payload)
    return db, repo


# ---------------------------------------------------------------------
# Test UPDATE logic
# ---------------------------------------------------------------------
def test_update_vehicle():
    db, repo = setup_sample()

    update_data = schemas.VehicleUpdate(
        manufacturer_name="Audi",
        description="Updated Sport",
        horse_power=260,
        model_name="A4",
        model_year=2021,
        purchase_price=32000.0,
        fuel_type="Hybrid"
    )

    updated_vehicle = repo.update("UPD1", update_data)

    assert updated_vehicle.horse_power == 260
    assert updated_vehicle.model_year == 2021
    assert updated_vehicle.description == "Updated Sport"
    assert updated_vehicle.fuel_type == "Hybrid"
