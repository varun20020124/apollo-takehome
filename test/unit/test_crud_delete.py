# test/unit/test_crud_delete.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.crud import VehicleRepository
from app import schemas

engine = create_engine("sqlite:///./unit_delete.db", connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def setup_sample():
    db = TestingSession()
    repo = VehicleRepository(db)

    payload = schemas.VehicleCreate(
        vin="DEL1",
        manufacturer_name="Ford",
        description="Truck",
        horse_power=400,
        model_name="F150",
        model_year=2019,
        purchase_price=45000.0,
        fuel_type="Diesel",
    )

    repo.create(payload)
    return db, repo


def test_delete_vehicle():
    db, repo = setup_sample()
    deleted = repo.delete("DEL1")
    assert deleted is True


def test_delete_nonexistent():
    db = TestingSession()
    repo = VehicleRepository(db)

    deleted = repo.delete("NOPE")
    assert deleted is None
