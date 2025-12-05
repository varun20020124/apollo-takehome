from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas, crud

app = FastAPI()

# Create Vehicle (POST)
@app.post("/vehicle", response_model=schemas.VehicleResponse, status_code=201)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    existing = crud.get_vehicle(db, vin=vehicle.vin.upper())
    if existing:
        raise HTTPException(status_code=400, detail=f"Vehicle with VIN {vehicle.vin.upper()} already exists.")
    
    return crud.create_vehicle(db, vehicle)

# Get ALL Vehicles (GET)
@app.get("/vehicle", response_model=list[schemas.VehicleResponse])
def get_all_vehicles(db: Session = Depends(get_db)):
    return crud.get_all_vehicles(db)

# Get ONE Vehicle (GET)
@app.get("/vehicle/{vin}", response_model=schemas.VehicleResponse)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    vehicle = crud.get_vehicle(db, vin.upper())
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

# Update Vehicle (PUT)
@app.put("/vehicle/{vin}", response_model=schemas.VehicleResponse)
def update_vehicle(vin: str, updates: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = crud.update_vehicle(db, vin.upper(), updates)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

# Delete Vehicle (DELETE)
@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    deleted = crud.delete_vehicle(db, vin.upper())
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None