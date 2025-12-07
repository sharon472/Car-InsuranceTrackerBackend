# Car Insurance Tracker: Frontend Application

A resilient, full-stack fleet management and insurance tracking application developed by **Sharon Njoroge**.

This repository contains the client-side application, built using **React** and **Vite**, which provides the administrative dashboard, handles all user interactions, and visualizes real-time vehicle status.

---

##  Project Overview

The **Car Insurance Tracker** is designed to eliminate the risks associated with manually monitoring critical vehicle documents in a commercial fleet. It provides administrators with a central, single source of truth for tracking insurance expiry dates, driver assignments, and overall vehicle health.

### Core Goals:

1.  **Risk Mitigation:** Provide clear, immediate visual warnings for vehicles with imminent or expired insurance coverage.
2.  **Operational Efficiency:** Enable fast and reliable **CRUD (Create, Read, Update, Delete)** management of all fleet vehicle records.
3.  **Full-Stack Resilience:** Ensure the user experience remains smooth even if temporary issues occur in the API or network layer.

---

## Key Features & Functionality

| Feature | Description | Technical Implementation |

| **Admin Authentication** | A dedicated login screen protects the application data and triggers data fetching upon successful sign-in. | Client-side validation using React hooks, connecting to the FastAPI `/login` endpoint. |

| **Real-time Dashboard** | Displays critical Key Performance Indicators (KPIs), such as **Total Fleet Count** and **Insurance Due Soon** (e.g., within 30 days). | Data aggregation logic performed over the main `cars` state array. |

| **Full CRUD Management** | Users can seamlessly add, edit, and delete vehicle records using a dedicated modal interface. | Handled by the core CRUD functions in `App.jsx`, which call the `services/api.js` layer. |

| **Resilient State Logic** | CRUD handlers include **API fall
| **Activity Log** | A chronological history of all critical user actions (login, car updates, deletions) and API synchronization status messages. | Uses a centralized `log` state, providing transparent debugging and audit history. |
| **Conditional Styling** | The `CarsTable` dynamically highlights records based on the insurance expiry date, providing visual alerts for urgent attention. | Logic implemented in `CarsTable.jsx` to apply classes based on date comparison. |

---

## Technical Stack

### Frontend (This Repository)

* **Framework:** **React**
* **Build Tool:** **Vite**

* **API Layer:** Custom `services/api.js` using asynchronous `fetch` for all backend communication.

### Backend (Required Dependency)

* **Framework:** **FastAPI** (Python)
* **Database:** **SQLAlchemy** (ORM) connected to a **SQLite** database (`cars.db`).
* **Security:** Configured with CORS Middleware to safely accept requests from the frontend origin.

---

##  Getting Started (Local Setup)

To run this application, you must start the backend API first.

### Step 1: Backend Setup & Running (FastAPI)

1.  Navigate to your backend repository directory (e.g., `cd ../backend`).
2.  Install required dependencies (assuming a `requirements.txt` is present):
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the FastAPI server:
    ```bash
    uvicorn app:app --reload
    ```
4.  *(Optional)* Ensure the database is populated by visiting: `http://127.0.0.1:8000/seed-data` in your browser.

### Step 2: Frontend Setup & Running (React)

1.  Navigate back to this frontend directory: `cd ../frontend`
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```

### Step 3: Access the Application

Open your browser to the local development server URL (usually `http://localhost:5173/`).

* **Login Credentials (Default Admin):**
    * **Username:** `admin`
    * **Password:** `1234`
    