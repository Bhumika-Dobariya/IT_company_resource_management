from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.managers import ManagerAll,UpdateManager
from src.models.manager import Manager
import uuid
from src.models.employee import Employee
from src.schemas.employee import EmployeeBase
from logs.log_config import logger



Managers = APIRouter(tags=["manager"])
db = Sessionlocal()


# Create manager

@Managers.post("/managers", response_model=ManagerAll)
def create_manager(manager: ManagerAll):
    db_manager = Manager(
        manager_id=str(uuid.uuid4()),
        name=manager.name, 
        role=manager.role,
        email=manager.email, 
        phone_number=manager.phone_number,
        department=manager.department, 
        address=manager.address,
        status=manager.status
    )
    
    db.add(db_manager)
    db.commit()
    logger.info(f"Created manager with ID: {db_manager.manager_id}")
    return db_manager



# Read manager

@Managers.get("/read_managers", response_model=ManagerAll)
def read_manager(manager_id: str):
    manager = db.query(Manager).filter(Manager.manager_id == manager_id, Manager.is_active == True, Manager.is_deleted == False).first()
    if manager is None:
        logger.warning(f"Manager not found for ID: {manager_id}")
        raise HTTPException(status_code=404, detail="Manager not found")
    logger.info(f"Retrieved manager with ID: {manager_id}")
    return manager



# Get managers by department

@Managers.get("/managers_department", response_model=List[ManagerAll])
def get_managers_by_department(department: str):
    db_managers = db.query(Manager).filter(Manager.department == department, Manager.is_active == True, Manager.is_deleted == False).all()
    logger.info(f"Retrieved managers for department: {department}")
    return db_managers



# Get all managers

@Managers.get("/list_of_managers", response_model=List[ManagerAll])
def list_managers():
    managers = db.query(Manager).filter(Manager.is_active == True, Manager.is_deleted == False).all()
    logger.info("Retrieved all managers")
    return managers



# Update manager

@Managers.patch("/update_managers", response_model=ManagerAll)
def update_manager_by_patch(manager_id: str, manager: UpdateManager):
    db_manager = db.query(Manager).filter(Manager.manager_id == manager_id, Manager.is_active == True, Manager.is_deleted == False).first()
    
    if db_manager is None:
        logger.warning(f"Manager not found for ID: {manager_id}")
        raise HTTPException(status_code=404, detail="Manager not found")
    
    if manager.name is not None:
        db_manager.name = manager.name
    if manager.email is not None:
        db_manager.email = manager.email
    if manager.phone_number is not None:
        db_manager.phone_number = manager.phone_number
    if manager.department is not None:
        db_manager.department = manager.department
    if manager.address is not None:
        db_manager.address = manager.address
    if manager.status is not None:
        db_manager.status = manager.status

    db.commit()
    db.refresh(db_manager)
    logger.info(f"Updated manager with ID: {manager_id}")
    return db_manager



# Delete manager

@Managers.delete("/managers", response_model=ManagerAll)
def delete_manager(manager_id: str):
    manager = db.query(Manager).filter(Manager.manager_id == manager_id, Manager.is_active == True, Manager.is_deleted == False).first()
    if manager is None:
        logger.warning(f"Manager not found for ID: {manager_id}")
        raise HTTPException(status_code=404, detail="Manager not found")
    
    db.delete(manager)
    db.commit()
    logger.info(f"Deleted manager with ID: {manager_id}")
    return manager



# Retrieve a list of employees who directly report to a specific manager

@Managers.get("/managers_all_emp_direct_reports", response_model=List[EmployeeBase])
def get_direct_reports(manager_id: str):
    employees = db.query(Employee).filter(
        Employee.manager_id == manager_id,
        Employee.is_active == True,
        Employee.is_deleted == False
    ).all()
    
    if not employees:
        logger.warning(f"No direct reports found for manager ID: {manager_id}")
        raise HTTPException(status_code=404, detail="No direct reports found for this manager")
    logger.info(f"Retrieved direct reports for manager ID: {manager_id}")
    return employees



# Assign a New Manager to an Employee

@Managers.patch("/employees_assign_manager", response_model=EmployeeBase)
def assign_manager_to_employee(employee_id: str, manager_id: str):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.is_active == True,
        Employee.is_deleted == False
    ).first()
    
    manager = db.query(Manager).filter(Manager.manager_id == manager_id, Manager.is_active == True).first()
    
    if employee is None:
        logger.warning(f"Employee not found for ID: {employee_id}")
        raise HTTPException(status_code=404, detail="Employee not found")
    if manager is None:
        logger.warning(f"Manager not found for ID: {manager_id}")
        raise HTTPException(status_code=404, detail="Manager not found")
    
    employee.manager_id = manager_id
    db.commit()
    logger.info(f"Assigned manager ID: {manager_id} to employee ID: {employee_id}")
    return employee



# Promote a manager by updating their role to a higher level

@Managers.patch("/managers_promote", response_model=ManagerAll)
def promote_manager(manager_id: str, new_role: str):
    manager = db.query(Manager).filter(Manager.manager_id == manager_id, Manager.is_active == True).first()
    
    if manager is None:
        logger.warning(f"Manager not found for ID: {manager_id}")
        raise HTTPException(status_code=404, detail="Manager not found")
    
    manager.role = new_role
    db.commit()
    db.refresh(manager)
    logger.info(f"Promoted manager with ID: {manager_id} to role: {new_role}")
    return manager