from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.events import CreateEvent,UpdateEvent
from src.models.event import Event
from logs.log_config import logger


events = APIRouter(tags=["Events"])
db = Sessionlocal()



@events.post("/events/", response_model=CreateEvent)
def create_event(event: CreateEvent):
    logger.info(f"Creating event: {event}")
    
    db_event = Event(
        name=event.name,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        organizer=event.organizer,
        type=event.type
    )
    db.add(db_event)
    db.commit()
    
    logger.info(f"Event created with ID: {db_event.id}")
    return db_event



@events.get("/read_event", response_model=CreateEvent)
def read_event(id: str):
    logger.info(f"Reading event with ID: {id}")
    
    event = db.query(Event).filter(Event.id == id, Event.is_active == True, Event.is_deleted == False).first()
    if event is None:
        logger.error(f"Event with ID {id} not found")
        raise HTTPException(status_code=404, detail="Event not found")
    
    logger.info(f"Event found: {event}")
    return event



@events.get("/list_of_event", response_model=List[CreateEvent])
def list_event():
    logger.info("Listing all active and not deleted events")
    
    events_list = db.query(Event).filter(Event.is_active == True, Event.is_deleted == False).all()
    
    logger.info(f"Number of events listed: {len(events_list)}")
    return events_list



@events.patch("/update_event", response_model=CreateEvent)
def update_event(id: str, event: UpdateEvent):
    logger.info(f"Updating event with ID: {id} with data: {event.dict()}")
    
    db_event = db.query(Event).filter(Event.id == id, Event.is_active == True, Event.is_deleted == False).first()
    if db_event is None:
        logger.error(f"Event with ID {id} not found")
        raise HTTPException(status_code=404, detail="Event not found")
    
    for field, value in event.dict(exclude_unset=True).items():
        setattr(db_event, field, value)
    
    db.commit()
    logger.info(f"Event with ID {id} updated")
    return db_event



@events.delete("/delete_event", response_model=CreateEvent)
def delete_event(id: str):
    logger.info(f"Deleting event with ID: {id}")
    
    db_event = db.query(Event).filter(Event.id == id, Event.is_active == True, Event.is_deleted == False).first()
    if db_event is None:
        logger.error(f"Event with ID {id} not found")
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_event.is_active = False
    db_event.is_deleted = True
    db.commit()
    
    logger.info(f"Event with ID {id} marked as deleted")
    return db_event



@events.get("/events_type/", response_model=List[CreateEvent])
def get_events_by_type(event_type: str):
    logger.info(f"Fetching events of type: {event_type}")
    
    db_events = db.query(Event).filter(
        Event.type == event_type,
        Event.is_deleted == False
    ).all()

    if not db_events:
        logger.error(f"No events found for type: {event_type}")
        raise HTTPException(status_code=404, detail="No events found for this type")

    logger.info(f"Found {len(db_events)} events of type: {event_type}")
    return db_events



@events.get("/events_organizer", response_model=List[CreateEvent])
def get_events_by_organizer(organizer_name: str):
    logger.info(f"Fetching events organized by: {organizer_name}")
    
    db_events = db.query(Event).filter(
        Event.organizer == organizer_name,
        Event.is_deleted == False
    ).all()

    if not db_events:
        logger.error(f"No events found for organizer: {organizer_name}")
        raise HTTPException(status_code=404, detail="No events found for this organizer")

    logger.info(f"Found {len(db_events)} events organized by: {organizer_name}")
    return db_events



@events.get("/events_count", response_model=dict)
def get_event_count():
    logger.info("Getting event count")
    
    count = db.query(Event).filter(Event.is_deleted == False).count()
    
    logger.info(f"Total number of events: {count}")
    return {"total_events": count}
