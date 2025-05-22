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


db = SessionLocal()
seed_roles(db)
db.close()