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
        Client (curl / browser / tests)
                   │
                   ▼
           FastAPI Application
               (app/main.py)
                   │
                   ▼
             CRUD Layer (app/crud.py)
        (pure DB operations / business logic)
                   │
                   ▼
 SQLAlchemy ORM Models & DB Session Management
     (app/models.py + app/database.py)
                   │
                   ▼
        SQLite Database File (vehicles.db)

- FastAPI handles HTTP routing, validation, and responses.

- Pydantic schemas define the request/response shapes and validation rules.

- SQLAlchemy maps Python classes (Vehicle) to database tables.

- Tests use TestClient and an isolated SQLite database.

---

## Repository Structure

1. app/  
   This folder holds all application source code:
   - database configuration  
   - SQLAlchemy models  
   - Pydantic schemas  
   - CRUD (database logic)  
   - FastAPI route definitions  

2. test/  
   This folder contains the automated test suite that uses pytest + TestClient.

Other important top-level files:
- requirements.txt → lists all dependencies
- README.md → project documentation
- pytest.ini → pytest configuration

## 🚀 Getting Started

Follow these steps to set up and run the Vehicle API locally.

---

### 1️⃣ **Clone the repository**

```bash
git clone https://github.com/your-username/apollo-takehome.git
cd apollo-takehome

### 2️⃣ **Create virtual environment and install requirements**
python3 -m venv venv
source venv/bin/activate     # Mac/Linux
# OR
venv\Scripts\activate        # Windows

pip install -r requirements.txt

### 3️⃣ **Initialize the database**

This project uses SQLite. The database file (vehicles.db) is automatically created when the API runs.

If you want to reset it run rm vehicles.db

### 4️⃣ **Run the API and test suite**

uvicorn app.main:app --reload
pytest -q
