from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

engine = create_engine("sqlite:///./unit_read.db", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def setup_sample():
    db = TestingSession()
    repo = crud.VehicleRepository(db)

    payload = schemas.VehicleCreate(
        vin="READ1",
        manufacturer_name="BMW",
        description="Luxury",
        horse_power=300,
        model_name="X5",
        model_year=2022,
        purchase_price=65000.0,
        fuel_type="Diesel"
    )
    repo.create(payload)
    return db, repo


def test_get_vehicle_by_vin():
    db, repo = setup_sample()
    v = repo.get("READ1")
    assert v.vin == "READ1"


def test_get_all_vehicles():
    db, repo = setup_sample()
    all_v = repo.list()
    assert len(all_v) == 1
