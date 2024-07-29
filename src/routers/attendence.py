from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.attendence import createattendence,updateattendence
from src.models.attaindance import Attendance
import uuid
from datetime import datetime
from logs.log_config import logger


Attendences = APIRouter(tags=["Attendence"])
db = Sessionlocal()


# ____________Create attendance record______________

@Attendences.post("/create_attendance", response_model=createattendence)
def create_attendance_record(attendance: createattendence):
   
    new_attendance = Attendance(
        id=str(uuid.uuid4()),
        employee_id=attendance.employee_id,
        check_in_time=attendance.check_in_time,
        check_out_time=attendance.check_out_time,
        is_present=attendance.is_present
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    logger.info(f"Created new attendance record: {new_attendance.id}")
    return new_attendance



# _______Read attendance record_______________

@Attendences.get("/read_attendance", response_model=createattendence)
def read_attendance_record(id: str):
    
    attendance = db.query(Attendance).filter(Attendance.id == id, Attendance.is_present == True).first()
    if attendance is None:
        logger.warning(f"Attendance record not found: {id}")
        raise HTTPException(status_code=404, detail="Attendance record not found")
    logger.info(f"Read attendance record: {id}")
    return attendance



# __________Read all attendance records__________

@Attendences.get("/read_ALL", response_model=List[createattendence])
def read_all_attendance_records():
  
    attendance = db.query(Attendance).filter(Attendance.is_present == True).all()
    if not attendance:
        logger.warning("No attendance records found")
        raise HTTPException(status_code=404, detail="Attendance record not found")
    logger.info("Read all attendance records")
    return attendance



# ___________Update attendance record___________

@Attendences.patch("/update_emp_attendence", response_model=createattendence)
def update_emp_attendence_by_patch(atn: updateattendence, id: str):
    
    db_attendence = db.query(Attendance).filter(Attendance.id == id, Attendance.is_present == True).first()
    if db_attendence is None:
        logger.warning(f"Attendance record not found for update: {id}")
        raise HTTPException(status_code=404, detail="Attendance record not found")

    for field_name, value in atn.dict().items():
        if value is not None:
            setattr(db_attendence, field_name, value)

    db.commit()
    logger.info(f"Updated attendance record: {id}")
    return db_attendence



# ___________Delete attendance record____________

@Attendences.delete("/delete_attendance", response_model=createattendence)
def delete_attendance_record(id: str):
    
    attendance = db.query(Attendance).filter(Attendance.id == id, Attendance.is_present == True).first()
    if attendance is None:
        logger.warning(f"Attendance record not found for deletion: {id}")
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    db.delete(attendance)
    db.commit()
    logger.info(f"Deleted attendance record: {id}")
    return attendance



# ________Get attendance records by employee____________

@Attendences.get("/attendance/employee", response_model=List[createattendence])
def get_attendance_by_employee(employee_id: str):
    
    db_attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id).all()
    if not db_attendance:
        logger.warning(f"No attendance records found for employee: {employee_id}")
        raise HTTPException(status_code=404, detail="No attendance records found for this employee")
    
    logger.info(f"Read attendance records for employee: {employee_id}")
    return db_attendance



# __________Get attendance summary by employee_____________

@Attendences.get("/attendance_employee_summary", response_model=dict)
def get_attendance_summary(employee_id: str):
    """
    # Attendance Summary
    Get attendance summary (total present and absent) for a specific employee.
    """
    total_present = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.is_present == True,
    ).count()
    
    total_absent = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.is_present == False,
    ).count()

    logger.info(f"Attendance summary for employee: {employee_id}")
    return {
        "total_present": total_present,
        "total_absent": total_absent
    }