# Collaborative Event Management System

A full-featured event management backend built with **FastAPI**, **SQLAlchemy**, and **Alembic**, supporting:

- User Authentication
- Event Creation & Ownership
- Event Sharing & Permission Control
- Event Versioning (Change History)
- RESTful APIs with Pydantic Schemas

---

## Features

- **User Auth**: Token-based authentication (OAuth2 with JWT)
- **Event CRUD**: Users can create, update, delete their events
- **Sharing & Permissions**: Share events with read/write access
- **Version History**: Every update to an event is tracked

---

## Project Structure

app/
├── api/ # API routes (FastAPI routers)
│ └── v1/
│ └── event.py
├── core/ # Configuration & database
│ └── database.py
├── models/ # SQLAlchemy models
│ ├── user.py
│ ├── event.py
│ └── event_version.py
├── schemas/ # Pydantic schemas
│ └── event.py
├── main.py # FastAPI app entrypoint
alembic/ # Alembic migrations


---

## Requirements

- Python 3.9+
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- Pydantic
- SQLite (or PostgreSQL)

### Running the App
Install dependencies:

```bash
pip install -r requirements.txt
```
### Configure Environment Variables
```bash
Create a .env file in the root directory:
DATABASE_URL=sqlite:///./app.db  
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```
### Run Database Migrations
```bash
alembic init alembic
```
Apply migrations:
```bash
alembic upgrade head
alembic revision --autogenerate -m "Add new models"
alembic upgrade head

```

### Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

### API Endpoints
| Method | Endpoint                      | Description                 |
| ------ | ----------------------------- | --------------------------- |
| POST   | `/events/`                    | Create event                |
| GET    | `/events/`                    | List your events            |
| PUT    | `/events/{event_id}`          | Update an event             |
| DELETE | `/events/{event_id}`          | Delete an event             |
| GET    | `/events/{event_id}/versions` | Get event version history   |
| POST   | `/events/{event_id}/share`    | Share event with a user     |

###  Event Versioning
Every time a user updates an event, a snapshot is saved to the event_versions table, including:

* Title

* Description

* Location

* Start and End Time

* Updated By

* Timestamp


