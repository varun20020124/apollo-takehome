# 🚗 Apollo Vehicle Service

A small FastAPI-based web service that exposes **CRUD-style REST APIs** for managing vehicles stored in a SQLite database.  
This project was implemented as a take-home exercise, focusing on:

- Clean, understandable architecture
- Clear separation of concerns
- API & DB correctness
- Automated tests runnable from the command line

---
```text
🧱 High-Level Architecture

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

Follow the steps below to set up and run the project locally.

---

1️⃣ Clone the Repository

git clone https://github.com/varun20020124/apollo-takehome.git
cd apollo-takehome

---

2️⃣ Create & Activate a Virtual Environment (recommended)

# Create a venv
python3 -m venv venv

# Activate it (macOS / Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

---

3️⃣ Install Dependencies

pip install -r requirements.txt

---

4️⃣ Run the FastAPI Application

uvicorn app.main:app --reload

The API will now be available at:

http://127.0.0.1:8000

Interactive Swagger docs:
http://127.0.0.1:8000/docs

---

5️⃣ Run the Test Suite

pytest -q

This will execute:
- Unit tests (tests/unit/)
- Component tests (tests/component/)

---

6️⃣ Project Structure Overview

app/
  - main.py → FastAPI routes & API layer
  - crud.py → Database operations & business logic (OOP repository pattern)
  - models.py → SQLAlchemy ORM models
  - schemas.py → Pydantic request/response validation schemas
  - database.py → Engine, session factory, Base class

tests/
  - unit/ → Unit tests for CRUD logic (pure Python + DB)
  - component/ → Full API-level tests using TestClient

requirements.txt → All required Python dependencies
