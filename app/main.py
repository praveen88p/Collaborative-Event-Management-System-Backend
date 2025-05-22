from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth,events
from app.core.database import SessionLocal
from app.core.seed_roles import seed_roles


Base.metadata.create_all(bind=engine)

app = FastAPI(title="NeoFi Event Manager")
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])

@app.get("/")
def read_root():
    return {"message": "NeoFi Event Management Backend"}

# Alembic Setup (CLI)
# 1. alembic init alembic
# 2. edit alembic.ini and env.py for proper path and target_metadata
# 3. alembic revision --autogenerate -m "Initial tables"
# 4. alembic upgrade head


db = SessionLocal()
seed_roles(db)
db.close()