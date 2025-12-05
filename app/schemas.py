from pydantic import BaseModel, Field
from typing import Optional

# Base schema (shared attributes)
class VehicleBase(BaseModel):
    manufacturer_name: str
    description: Optional[str] = None
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str


# Schema for creating a vehicle (POST)
class VehicleCreate(VehicleBase):
    vin: str = Field(..., description="Unique Vehicle Identification Number")

# Schema for updating a vehicle (PUT)
# VIN is not included because it is passed in the URL path
class VehicleUpdate(VehicleBase):
    pass

# Schema for API responses
class VehicleResponse(VehicleBase):
    vin: str

    class Config:
        from_attributes = True   # allows Pydantic to read SQLAlchemy models
