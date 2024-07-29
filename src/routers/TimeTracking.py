from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.TimeTracking import CreateTimeTracking,UpdateTimeTracking
from src.models.TimeTracking import TimeTracking
from src.models.employee import Employee
import uuid
from datetime import datetime
from typing import List,Dict
from logs.log_config import logger


Timetracking = APIRouter(tags=["TimeTracking"])
db = Sessionlocal()


@Timetracking.post("/create_time_tracking", response_model=CreateTimeTracking)
def create_time_tracking_entry(time_tracking: CreateTimeTracking):
    logger.info(f"Creating time tracking entry for employee ID: {time_tracking.emp_id} on date: {time_tracking.date}")
    
    employee = db.query(Employee).filter(Employee.id == time_tracking.emp_id).first()
    if not employee:
        logger.error(f"Employee with ID {time_tracking.emp_id} not found")
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_time_tracking = TimeTracking(
        id=str(uuid.uuid4()),
        emp_id=time_tracking.emp_id,
        date=time_tracking.date,
        check_in_time=time_tracking.check_in_time,
        check_out_time=time_tracking.check_out_time,
        hours_worked=time_tracking.hours_worked,
        status=time_tracking.status,
        extra_hours=time_tracking.extra_hours
    )
    db.add(db_time_tracking)
    db.commit()
    logger.info(f"Time tracking entry created with ID: {db_time_tracking.id}")
    return db_time_tracking



@Timetracking.get("/get_all", response_model=List[CreateTimeTracking])
def get_all_tasks():
    logger.info("Fetching all time tracking entries")
    time_tracking_entries = db.query(TimeTracking).all()
    if not time_tracking_entries:
        logger.error("No time tracking records found")
        raise HTTPException(status_code=404, detail="TimeTracking not found")
    return time_tracking_entries



@Timetracking.patch("/update_timetracking_by_patch", response_model=CreateTimeTracking)
def update_timetracking_by_patch(id: str, timetracking: UpdateTimeTracking):
    logger.info(f"Updating time tracking entry with ID: {id}")
    db_time_tracking = db.query(TimeTracking).filter(TimeTracking.id == id).first()
    if db_time_tracking is None:
        logger.error(f"Time tracking entry with ID {id} not found")
        raise HTTPException(status_code=404, detail="TimeTracking not found")

    for field_name, value in timetracking.dict().items():
        if value is not None:
            setattr(db_time_tracking, field_name, value)
    db.commit()
    logger.info(f"Time tracking entry with ID {id} updated successfully")
    return db_time_tracking



@Timetracking.delete("/delete_Timetracking")
def delete_timetracking(id: str):
    logger.info(f"Deleting time tracking entry with ID: {id}")
    db_time_tracking = db.query(TimeTracking).filter(TimeTracking.id == id).first()
    if db_time_tracking is None:
        logger.error(f"Time tracking entry with ID {id} not found")
        raise HTTPException(status_code=404, detail="TimeTracking not found")
    db.delete(db_time_tracking)
    db.commit()
    logger.info(f"Time tracking entry with ID {id} deleted successfully")
    return {"message": "TimeTracking deleted successfully"}



@Timetracking.get("/time_tracking_employee", response_model=List[CreateTimeTracking])
def get_time_tracking_by_employee(emp_id: str):
    logger.info(f"Fetching time tracking records for employee ID: {emp_id}")
    db_time_tracking = db.query(TimeTracking).filter_by(emp_id=emp_id).all()
    if not db_time_tracking:
        logger.error(f"No time tracking records found for employee ID {emp_id}")
        raise HTTPException(status_code=404, detail="No time tracking records found for this employee")
    return db_time_tracking



@Timetracking.get("/time_tracking_date_range", response_model=List[CreateTimeTracking])
def get_time_tracking_by_date_range(start_date: datetime, end_date: datetime):
    logger.info(f"Fetching time tracking records from {start_date} to {end_date}")
    db_time_tracking = db.query(TimeTracking).filter(
        TimeTracking.date >= start_date,
        TimeTracking.date <= end_date
    ).all()
    if not db_time_tracking:
        logger.error(f"No time tracking records found for the date range from {start_date} to {end_date}")
        raise HTTPException(status_code=404, detail="No time tracking records found for this date range")
    return db_time_tracking



@Timetracking.get("/time_tracking_total_hours_employee", response_model=Dict[str, float])
def get_total_hours_worked(emp_id: str, start_date: str, end_date: str):
    logger.info(f"Calculating total hours worked for employee ID: {emp_id} from {start_date} to {end_date}")
    time_tracking_records = db.query(TimeTracking).filter(
        TimeTracking.emp_id == emp_id,
        TimeTracking.date >= start_date,
        TimeTracking.date <= end_date
    ).all()
    
    total_hours = 0.0
    for record in time_tracking_records:
        if record.hours_worked is not None:
            total_hours += record.hours_worked

    logger.info(f"Total hours worked for employee ID: {emp_id} from {start_date} to {end_date} is {total_hours}")
    return {"total_hours_worked": total_hours}