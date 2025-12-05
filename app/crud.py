from sqlalchemy.orm import Session
from . import models, schemas


class VehicleRepository:
    """
    A small repository class that encapsulates all database operations
    related to the Vehicle entity.

    This keeps DB logic in one place and makes it easier to understand,
    test, and extend later.
    """

    def __init__(self, db: Session):
        self.db = db

    def _normalize_vin(self, vin: str) -> str: # helper to normalise vin
        return vin.strip().upper()

    def get(self, vin: str): # read single
        norm_vin = self._normalize_vin(vin)
        return (
            self.db.query(models.Vehicle)
            .filter(models.Vehicle.vin == norm_vin)
            .first()
        )

    def list(self): # read all
        return self.db.query(models.Vehicle).all()

    def create(self, vehicle: schemas.VehicleCreate): # create
        norm_vin = self._normalize_vin(vehicle.vin)

        # Check if VIN already exists (case-insensitive)
        existing = self.get(vehicle.vin)
        if existing:
            return None  # main.py will raise 400

        new_vehicle = models.Vehicle(
            vin=norm_vin,
            manufacturer_name=vehicle.manufacturer_name,
            description=vehicle.description,
            horse_power=vehicle.horse_power,
            model_name=vehicle.model_name,
            model_year=vehicle.model_year,
            purchase_price=vehicle.purchase_price,
            fuel_type=vehicle.fuel_type,
        )

        self.db.add(new_vehicle)
        self.db.commit()
        self.db.refresh(new_vehicle)
        return new_vehicle

    def update(self, vin: str, update_data: schemas.VehicleUpdate): # update
        vehicle = self.get(vin)
        if not vehicle:
            return None

        update_dict = update_data.model_dump() # using model dump instead of dict just in case of update

        for field, value in update_dict.items():
            setattr(vehicle, field, value)

        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vin: str): # delete
        vehicle = self.get(vin)
        if not vehicle:
            return None

        self.db.delete(vehicle)
        self.db.commit()
        return True