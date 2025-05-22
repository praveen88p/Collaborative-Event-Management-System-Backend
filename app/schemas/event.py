# app/schemas/event.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventOut(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Updated from 'orm_mode' for Pydantic v2
