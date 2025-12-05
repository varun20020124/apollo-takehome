"""
1. Defines all HTTP routes (POST, GET, PUT, DELETE) for the /vehicle API.
2. Injects a database session using Depends(get_db) on every request.
3. Uses VehicleRepository to perform business logic and DB operations.
4. Raises appropriate HTTP errors (400, 404) using HTTPException.
5. Controls the flow of request → validation → business logic → response.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models, schemas, crud
from .crud import VehicleRepository

# Create all database tables at startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/vehicle", response_model=schemas.VehicleResponse, status_code=201)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    """Create a new vehicle if VIN does not already exist."""
    repo = VehicleRepository(db)

    if repo.get(vehicle.vin):  # check VIN uniqueness
        raise HTTPException(
            status_code=400,
            detail=f"Vehicle with VIN {vehicle.vin.upper()} already exists."
        )

    return repo.create(vehicle)


@app.get("/vehicle", response_model=list[schemas.VehicleResponse])
def get_all_vehicles(db: Session = Depends(get_db)):
    """Retrieve all vehicles in the database."""
    repo = VehicleRepository(db)
    return repo.list()


@app.get("/vehicle/{vin}", response_model=schemas.VehicleResponse)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    """Retrieve a single vehicle by VIN."""
    repo = VehicleRepository(db)
    vehicle = repo.get(vin)

    if not vehicle:  # handle not found
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@app.put("/vehicle/{vin}", response_model=schemas.VehicleResponse)
def update_vehicle(vin: str, updates: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    """Update an existing vehicle using its VIN."""
    repo = VehicleRepository(db)
    updated = repo.update(vin, updates)

    if not updated:  # handle nonexistent VIN
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return updated


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    """Delete a vehicle by VIN."""
    repo = VehicleRepository(db)
    deleted = repo.delete(vin)

    if not deleted:  # handle nonexistent VIN
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return None
