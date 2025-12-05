from sqlalchemy.orm import Session
from . import models, schemas

# CREATE
def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    # Convert VIN to uppercase for consistency
    vin = vehicle.vin.upper()

    # Check if VIN already exists
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if db_vehicle:
        return None  # main.py will handle the error

    new_vehicle = models.Vehicle(
        vin=vin,
        manufacturer_name=vehicle.manufacturer_name,
        description=vehicle.description,
        horse_power=vehicle.horse_power,
        model_name=vehicle.model_name,
        model_year=vehicle.model_year,
        purchase_price=vehicle.purchase_price,
        fuel_type=vehicle.fuel_type
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

# READ (GET ALL)
def get_all_vehicles(db: Session):
    return db.query(models.Vehicle).all()

# # READ (GET BY VIN)
# def get_vehicle_by_vin(db: Session, vin: str):
#     return db.query(models.Vehicle).filter(models.Vehicle.vin == vin.upper()).first()

# READ (GET BY VIN)
def get_vehicle_by_vin(db: Session, vin: str):
    return db.query(models.Vehicle).filter(models.Vehicle.vin == vin.upper()).first()

# wrapper so main.py and tests can call crud.get_vehicle()
def get_vehicle(db: Session, vin: str):
    return get_vehicle_by_vin(db, vin)

# UPDATE
def update_vehicle(db: Session, vin: str, update_data: schemas.VehicleUpdate):
    db_vehicle = get_vehicle_by_vin(db, vin)
    if not db_vehicle:
        return None

    for field, value in update_data.dict().items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# DELETE
def delete_vehicle(db: Session, vin: str):
    db_vehicle = get_vehicle_by_vin(db, vin)
    if not db_vehicle:
        return None

    db.delete(db_vehicle)
    db.commit()
    return True