# Car Insurance Tracker: Backend API

A high-performance **RESTful API** built with **FastAPI** to serve vehicle, employee, and insurance data for the Car Insurance Tracker application.

**Developed by:** Sharon Njoroge

---

##  Overview & Purpose

This repository contains the server-side logic and data persistence layer. It provides a secure and reliable interface for the React frontend, handling all data storage and retrieval operations.

### Core Functions:

1.  **Data Persistence:** Manages **SQLAlchemy** ORM definitions and handles CRUD operations on the SQLite database (`cars.db`).
2.  **RESTful Service:** Exposes robust and fast endpoints for all fleet management data.
3.  **Security:** Implements necessary CORS policies to safely communicate with the frontend client.

---

##  Technical Stack

| Component | Technology | Role in Project |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** (Python) | High-speed API development, routing, and Pydantic data validation. |
| **Database** | **SQLAlchemy** | Object-Relational Mapper (ORM) for defining schema and executing queries. |
| **Server** | **Uvicorn** | Asynchronous Server Gateway Interface (ASGI) used to serve the FastAPI app. |
| **Security** | **CORS Middleware** | Configured in `app.py` to allow secure cross-origin requests from the React client. |

---

##  Getting Started (Local Setup)

Follow these steps to set up and run the API locally.

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 2. Clone Repository & Setup Environment

1.  Clone this repository.
2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  
    ```
3.  Install all required dependencies:
    ```bash
    pip install -r requirements.txt 
    # Or manually: pip install fastapi uvicorn 'sqlalchemy<2.0' alembic python-dotenv
    ```

### 3. Initialize Database & Seed Data

1.  **Run Migrations:** Initialize the database structure defined by your SQLAlchemy models:
    ```bash
    alembic upgrade head
    ```
2.  **Seed Data:** Start the server, then manually open `http://127.0.0.1:8000/seed-data` in your browser to populate the `cars.db` file with initial testing records.

### 4. Running the Server

Start the API server using Uvicorn. The server will run on `http://127.0.0.1:8000`.

```bash
uvicorn app:app --reload