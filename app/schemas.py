from pydantic import BaseModel, Field
from typing import Optional

# Shared fields across Create, Update, Response
class VehicleBase(BaseModel):
    manufacturer_name: str
    description: Optional[str] = None
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str


class VehicleCreate(VehicleBase):
    """Request body for creating a vehicle."""
    vin: str = Field(..., description="Unique Vehicle Identification Number")


class VehicleUpdate(VehicleBase):
    """Request body for updating a vehicle (VIN excluded)."""
    pass


class VehicleResponse(VehicleBase):
    """Response model returned to clients."""
    vin: str

    class Config:
        from_attributes = True  # enables ORM → Pydantic conversion
