# File: app/routes/events.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventOut
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.event import Event
from app.models.permission import EventPermission
from typing import List, Optional
from sqlalchemy import or_

router = APIRouter()

@router.post("/", response_model=EventOut)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Validate time logic
    if event_in.end_time <= event_in.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    # Create event
    event = Event(
        title=event_in.title,
        description=event_in.description,
        start_time=event_in.start_time,
        end_time=event_in.end_time,
        location=event_in.location,
        is_recurring=event_in.is_recurring,
        recurrence_pattern=event_in.recurrence_pattern,
        owner_id=current_user.id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # Add permission entry as Owner
    perm = EventPermission(user_id=current_user.id, event_id=event.id, role="Owner")
    db.add(perm)
    db.commit()

    return event


@router.get("/", response_model=List[EventOut])
def list_events(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    title: Optional[str] = None,
    start_after: Optional[datetime] = None,
    end_before: Optional[datetime] = None,
):
    # Join with EventPermission to filter by access
    query = db.query(Event).join(EventPermission).filter(EventPermission.user_id == current_user.id)

    # Optional filters
    if title:
        query = query.filter(Event.title.ilike(f"%{title}%"))
    if start_after:
        query = query.filter(Event.start_time >= start_after)
    if end_before:
        query = query.filter(Event.end_time <= end_before)

    events = query.offset(offset).limit(limit).all()
    return events
