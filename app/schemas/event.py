# app/schemas/event.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventOut(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Updated from 'orm_mode' for Pydantic v2






import sqlite3

# Adjust the path to your SQLite DB file
conn = sqlite3.connect("dev.db")  # or whatever your DB file is called
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='event_versions';")
result = cursor.fetchone()

if result:
    print("Table exists:", result[0])
else:
    print("Table does NOT exist.")

conn.close()
