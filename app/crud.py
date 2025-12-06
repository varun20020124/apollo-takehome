# Contains the VehicleRepository class, which encapsulates all DB operations and 
# Centralises data access logic 
"""
1. Implements the VehicleRepository class for clean CRUD operations.
2. Normalizes VIN (uppercase) before any DB interaction.
3. Provides get(), list(), create(), update(), delete() methods.
4. Encapsulates all DB logic so routes stay clean and modular.
"""
from sqlalchemy.orm import Session
from . import models, schemas


class VehicleRepository:
    """
    Repository class that encapsulates all database operations
    for Vehicle objects.
    """

    def __init__(self, db: Session):
        self.db = db  # database session

    def _normalize_vin(self, vin: str) -> str:
        """Normalize VIN input for consistent DB lookups."""
        return vin.strip().upper()

    def get(self, vin: str):
        """Fetch a single vehicle by VIN."""
        norm_vin = self._normalize_vin(vin)
        return (
            self.db.query(models.Vehicle)
            .filter(models.Vehicle.vin == norm_vin)
            .first()
        )

    def list(self):
        """Return all vehicles in the database."""
        return self.db.query(models.Vehicle).all()

    def create(self, vehicle: schemas.VehicleCreate):
        """Insert a new vehicle if VIN does not already exist."""
        norm_vin = self._normalize_vin(vehicle.vin)

        existing = self.get(vehicle.vin)
        if existing:
            return None  # main.py will raise the HTTP 400

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

    def update(self, vin: str, update_data: schemas.VehicleUpdate):
        """Update fields of an existing vehicle."""
        vehicle = self.get(vin)
        if not vehicle:
            return None

        update_dict = update_data.model_dump()

        for field, value in update_dict.items():
            setattr(vehicle, field, value)

        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vin: str):
        """Delete a vehicle by VIN."""
        vehicle = self.get(vin)
        if not vehicle:
            return None

        self.db.delete(vehicle)
        self.db.commit()
        return True