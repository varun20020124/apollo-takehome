from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas
from .crud import VehicleRepository

app = FastAPI()

@app.post("/vehicle", response_model=schemas.VehicleResponse, status_code=201)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    repo = VehicleRepository(db)

    if repo.get(vehicle.vin):
        raise HTTPException(
            status_code=400,
            detail=f"Vehicle with VIN {vehicle.vin.upper()} already exists."
        )

    return repo.create(vehicle)


@app.get("/vehicle", response_model=list[schemas.VehicleResponse])
def get_all_vehicles(db: Session = Depends(get_db)):
    repo = VehicleRepository(db)
    return repo.list()


@app.get("/vehicle/{vin}", response_model=schemas.VehicleResponse)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    repo = VehicleRepository(db)
    vehicle = repo.get(vin)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@app.put("/vehicle/{vin}", response_model=schemas.VehicleResponse)
def update_vehicle(vin: str, updates: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    repo = VehicleRepository(db)
    updated = repo.update(vin, updates)

    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return updated


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    repo = VehicleRepository(db)
    deleted = repo.delete(vin)

    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return None