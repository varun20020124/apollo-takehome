from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

# ----------------------------------------
# Setup test database
# ----------------------------------------
engine = create_engine(
    "sqlite:///./unit_create.db",
    connect_args={"check_same_thread": False}
)
TestingSession = sessionmaker(bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def test_create_vehicle():
    db = TestingSession()

    repo = crud.VehicleRepository(db)

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

    result = repo.create(payload)
    assert result.vin == "XYZ111"
    assert result.model_name == "Civic"
    assert result.horse_power == 120


def test_create_duplicate_vehicle():
    db = TestingSession()

    repo = crud.VehicleRepository(db)

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

    repo.create(payload)
    duplicate = repo.create(payload)

    # In OOP CRUD, you decide behavior; returning None is fine
    assert duplicate is None
