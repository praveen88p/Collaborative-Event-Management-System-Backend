from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventOut, EventUpdate
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.event import Event
from app.models.permission import EventPermission
from typing import List, Optional
from sqlalchemy import or_
from datetime import datetime
from app.models.user import User


router = APIRouter()

@router.post("/", response_model=EventOut)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    
    if event_in.end_time <= event_in.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    
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
    query = db.query(Event).join(EventPermission).filter(EventPermission.user_id == current_user.id)

    if title:
        query = query.filter(Event.title.ilike(f"%{title}%"))
    if start_after:
        query = query.filter(Event.start_time >= start_after)
    if end_before:
        query = query.filter(Event.end_time <= end_before)

    events = query.offset(offset).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=EventOut)
def get_event_by_id(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    permission = db.query(EventPermission).filter_by(
        user_id=current_user.id, event_id=event_id
    ).first()
    if not permission:
        raise HTTPException(status_code=403, detail="Permission denied")

    event = db.query(Event).filter_by(id=event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event


@router.put("/{id}", response_model=EventOut)
def update_event(
    id: int,
    event_in: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    permission = db.query(EventPermission).filter_by(event_id=id, user_id=current_user.id).first()
    if not permission or permission.role not in ["Owner", "Editor"]:
        raise HTTPException(status_code=403, detail="You don't have permission to edit this event")

   
    from app.models.event_version import EventVersion
    version = EventVersion(
        event_id=event.id,
        title=event.title,
        description=event.description,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time,
        updated_by=current_user.id
    )
    db.add(version)

   
    event.title = event_in.title
    event.description = event_in.description
    event.location = event_in.location
    event.start_time = event_in.start_time
    event.end_time = event_in.end_time
    event.is_recurring = event_in.is_recurring
    event.recurrence_pattern = event_in.recurrence_pattern

    db.commit()
    db.refresh(event)

    return event
