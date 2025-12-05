# 🚗 Apollo Vehicle Service

A small FastAPI-based web service that exposes **CRUD-style REST APIs** for managing vehicles stored in a SQLite database.  
This project was implemented as a take-home exercise, focusing on:

- Clean, understandable architecture
- Clear separation of concerns
- API & DB correctness
- Automated tests runnable from the command line

---

## 🧱 High-Level Architecture
```text
Client (curl / browser / automated tests)
                   │
                   ▼
           FastAPI Application
               (app/main.py)
     - Handles routing, validation, dependency injection
     - Converts Python objects ↔ JSON responses
                   │
                   ▼
        Service / CRUD Layer (app/crud.py)
     - Encapsulates business logic and data operations
     - Interacts with the database via SQLAlchemy ORM
                   │
                   ▼
 SQLAlchemy Models & DB Session Management
    (app/models.py + app/database.py)
     - Defines database tables and fields
     - Manages DB engine, sessions, and connections
                   │
                   ▼
            SQLite Database (vehicles.db)
     - Lightweight persistent storage for vehicles


- FastAPI handles HTTP routing, validation, and responses.

- Pydantic schemas define the request/response shapes and validation rules.

- SQLAlchemy maps Python classes (Vehicle) to database tables.

- Tests use TestClient and an isolated SQLite database.

---

Repository Structure

app/ -> This folder holds all application source code
main.py : Defines all API endpoints (POST, GET, PUT, DELETE) using FastAPI and connects them to the CRUD layer.

crud.py : Contains all database-facing logic (create, read, update, delete) using the VehicleRepository class.

models.py : Defines the SQLAlchemy ORM model (`Vehicle`) representing the `vehicles` table.

schemas.py : Defines Pydantic models used for request validation and response serialization.

database.py : Configures the SQLite database, creates the engine/session, and provides the `get_db` dependency used by FastAPI.

tests/
unit/ -> unit tests
Contains isolated unit tests for CRUD operations—no FastAPI, only direct function-level testing.

component/ -> api tests
Contains component/integration tests that simulate real API calls using `TestClient` and a temporary SQLite database.

Other important top-level files:
- requirements.txt → lists all dependencies
- README.md → project documentation
- pytest.ini → pytest configuration

🚀 Getting Started

Follow these steps to set up and run the Vehicle API locally.

---

1️⃣ Clone the repository

git clone https://github.com/your-username/apollo-takehome.git
cd apollo-takehome

2️⃣ Create virtual environment and install requirements
python3 -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt

3️⃣ Initialize the database

This project uses SQLite. 

4️⃣ Run the API and test suite

uvicorn app.main:app --reload
pytest -q
