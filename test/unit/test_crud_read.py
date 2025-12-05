from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.crud import VehicleRepository
from app import schemas

# Setup isolated SQLite test DB
engine = create_engine(
    "sqlite:///./unit_read.db",
    connect_args={"check_same_thread": False}
)
TestingSession = sessionmaker(bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def setup_sample():
    """Create a sample vehicle in an isolated test DB."""
    db = TestingSession()
    repo = VehicleRepository(db)

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
    """Ensure fetching a vehicle by VIN returns the correct record."""
    db, repo = setup_sample()
    v = repo.get("READ1")
    assert v.vin == "READ1"
    assert v.model_name == "X5"


def test_get_all_vehicles():
    """Ensure list() returns all saved vehicles."""
    db, repo = setup_sample()
    vehicles = repo.list()
    assert len(vehicles) == 1
    assert vehicles[0].vin == "READ1"
