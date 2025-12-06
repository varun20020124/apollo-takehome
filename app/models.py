# ORM model
"""
1. Defines the Vehicle model, mapping Python attributes → SQL table columns.
2. Controls how data is stored in the vehicles table.
3. Enforces DB-level structure (types, nullable fields, primary key on VIN).
"""
from sqlalchemy import Column, String, Integer, Float
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles" # Name of the table in SQLite

    vin = Column(String, primary_key=True, index=True)
    manufacturer_name = Column(String, nullable=False)
    description = Column(String)
    horse_power = Column(Integer, nullable=False)
    model_name = Column(String, nullable=False)
    model_year = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    fuel_type = Column(String, nullable=False)
    color  = Column(String, nullable=False)