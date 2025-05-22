from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class EventPermission(Base):
    __tablename__ = "event_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    role = Column(String, nullable=False)  # 'Owner', 'Editor', 'Viewer'

    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_user_event"),)
