from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

# Create an isolated SQLite DB for this test file
engine = create_engine(
    "sqlite:///./unit_create.db",
    connect_args={"check_same_thread": False}
)

# Session factory bound to the test DB
TestingSession = sessionmaker(bind=engine)

# Reset DB tables before running tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def test_create_vehicle():
    db = TestingSession()
    repo = crud.VehicleRepository(db)   # use repository directly

    # Valid vehicle payload
    payload = schemas.VehicleCreate(
        vin="XYZ111",
        manufacturer_name="Honda",
        description="Compact",
        horse_power=120,
        model_name="Civic",
        model_year=2018,
        purchase_price=15000.0,
        fuel_type="Petrol"
    )

    # Create new vehicle
    result = repo.create(payload)

    # Assertions verify correct persistence
    assert result.vin == "XYZ111"
    assert result.model_name == "Civic"
    assert result.horse_power == 120


def test_create_duplicate_vehicle():
    db = TestingSession()
    repo = crud.VehicleRepository(db)

    # Same payload used twice to test duplicate handling
    payload = schemas.VehicleCreate(
        vin="XYZ111",
        manufacturer_name="Honda",
        description="Compact",
        horse_power=120,
        model_name="Civic",
        model_year=2018,
        purchase_price=15000.0,
        fuel_type="Petrol"
    )

    repo.create(payload)               # first insert succeeds
    duplicate = repo.create(payload)   # duplicate VIN should fail

    # Repo returns None for duplicates (FastAPI layer turns this into HTTP 400)
    assert duplicate is None
