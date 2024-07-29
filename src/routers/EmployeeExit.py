from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.EmployeeExit import NEmployeeExit
from src.models.EmployeeExit import EmployeeExit
from datetime import date
from logs.log_config import logger


empexit = APIRouter(tags=["EmployeeExit"])
db = Sessionlocal()



# ____________Create employee exit____________

@empexit.post("/employee_exits", response_model=NEmployeeExit)
def create_employee_exit(employee_exit: NEmployeeExit):
    db_employee_exit = EmployeeExit(
        employee_id=employee_exit.employee_id,
        exit_date=employee_exit.exit_date,
        reason_for_exit=employee_exit.reason_for_exit
    )

    db.add(db_employee_exit)
    db.commit()
    db.refresh(db_employee_exit)
    logger.info(f"Created employee exit record for employee ID: {employee_exit.employee_id}")
    return db_employee_exit



# ____________Get employee exit by ID____________

@empexit.get("/get_employee_exits_by_id", response_model=NEmployeeExit)
def get_employee_exit_by_id(exit_id: str):
    db_employee_exit = db.query(EmployeeExit).filter(EmployeeExit.id == exit_id).first()
    if db_employee_exit is None:
        logger.warning(f"Employee exit not found for ID: {exit_id}")
        raise HTTPException(status_code=404, detail="Employee exit not found")
    logger.info(f"Retrieved employee exit record for ID: {exit_id}")
    return db_employee_exit



# __________Get all employee exits___________

@empexit.get("/get_all_employee_exits", response_model=List[NEmployeeExit])
def get_all_employee_exits():
    db_employee_exits = db.query(EmployeeExit).all()
    logger.info("Retrieved all employee exit records")
    return db_employee_exits


# _________Update employee exit_____________

@empexit.put("/update_employee_exits", response_model=NEmployeeExit)
def update_employee_exit(id: int, employee_exit_update: NEmployeeExit):
    db_employee_exit = db.query(EmployeeExit).filter(EmployeeExit.id == id).first()

    if not db_employee_exit:
        logger.warning(f"Employee exit not found for update, ID: {id}")
        raise HTTPException(status_code=404, detail="Employee exit not found")

    db_employee_exit.employee_id = employee_exit_update.employee_id
    db_employee_exit.exit_date = employee_exit_update.exit_date
    db_employee_exit.reason_for_exit = employee_exit_update.reason_for_exit

    db.commit()
    db.refresh(db_employee_exit)
    logger.info(f"Updated employee exit record for ID: {id}")
    return db_employee_exit


# _________Delete employee exit_______

@empexit.delete("/delete_employee_exits", response_model=NEmployeeExit)
def delete_employee_exit(id: int):
    db_employee_exit = db.query(EmployeeExit).filter(EmployeeExit.id == id).first()

    if not db_employee_exit:
        logger.warning(f"Employee exit not found for deletion, ID: {id}")
        raise HTTPException(status_code=404, detail="Employee exit not found")

    db.delete(db_employee_exit)
    db.commit()
    logger.info(f"Deleted employee exit record for ID: {id}")
    return db_employee_exit



# ___________Get employee exit records by employee ID_____________

@empexit.get("/employee_exit_by_employee_id", response_model=List[NEmployeeExit])
def get_employee_exits_by_employee_id(employee_id: str):
    db_employee_exits = db.query(EmployeeExit).filter(EmployeeExit.employee_id == employee_id).all()

    if not db_employee_exits:
        logger.warning(f"No exit records found for employee ID: {employee_id}")
        raise HTTPException(status_code=404, detail="No exit records found for this employee")
    logger.info(f"Retrieved exit records for employee ID: {employee_id}")
    return db_employee_exits



# __________Count employee exit records by reason_________

@empexit.get("/employee_exit_count_by_reason", response_model=dict)
def count_employee_exits_by_reason(reason: str):
    count = db.query(EmployeeExit).filter(EmployeeExit.reason_for_exit == reason).count()
    logger.info(f"Counted {count} exit records for reason: {reason}")
    return {"count": count}