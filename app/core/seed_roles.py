from sqlalchemy.orm import Session
from app.models.role import Role

def seed_roles(db: Session):
    roles = ["Owner", "Editor", "Viewer"]
    for role_name in roles:
        if not db.query(Role).filter_by(name=role_name).first():
            db.add(Role(name=role_name))
    db.commit()