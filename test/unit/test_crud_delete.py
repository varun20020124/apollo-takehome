from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.crud import VehicleRepository
from app import schemas

# Create a dedicated SQLite DB for delete-operation unit tests
engine = create_engine("sqlite:///./unit_delete.db", connect_args={"check_same_thread": False})

# Create a session factory bound to the test DB
TestingSession = sessionmaker(bind=engine)

# Reset the tables to ensure clean test runs
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def setup_sample():
    """Create one sample vehicle in the test DB and return (db, repo)."""
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
    """Ensure a valid VIN is deleted successfully."""
    db, repo = setup_sample()
    deleted = repo.delete("DEL1")
    assert deleted is True


def test_delete_nonexistent():
    """Ensure deleting a non-existent VIN returns None."""
    db = TestingSession()
    repo = VehicleRepository(db)

    deleted = repo.delete("NOPE")
    assert deleted is None
