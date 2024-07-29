from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.employee import EmployeeBase,EmployeeUpdate
from datetime import datetime
from src.models.employee import Employee
import uuid
from logs.log_config import logger

emp = APIRouter(tags=["Employee"])
db = Sessionlocal()


# _________Create employee_________

@emp.post("/create_employees", response_model=EmployeeBase)
def create_employee(employee: EmployeeBase):
    db_employee = Employee(
        id=str(uuid.uuid4()),
        manager_id=employee.manager_id,
        name=employee.name,
        email=employee.email,
        position=employee.position,
        role=employee.role,
        department=employee.department,
        address=employee.address,
        DOB=employee.DOB,
        date_hired=datetime.now(),
        phone_number=employee.phone_number,
        salary=employee.salary,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    logger.info(f"Created new employee: {employee.name} ({db_employee.id})")
    return db_employee



# ___________Get employee____________

@emp.get("/get_employee", response_model=EmployeeBase)
def get_employee(id: str):
    db_emp = db.query(Employee).filter(Employee.id == id, Employee.is_active == True, Employee.is_deleted == False).first()
    if db_emp is None:
        logger.warning(f"Employee not found: {id}")
        raise HTTPException(status_code=404, detail="Employee not found")
    logger.info(f"Read employee record: {id}")
    return db_emp



# _________Get all employees____________

@emp.get("/get_all_employee", response_model=List[EmployeeBase])
def get_all_employee():
    db_emp = db.query(Employee).filter(Employee.is_active == True, Employee.is_deleted == False).all()
    if not db_emp:
        logger.warning("No active employees found")
        raise HTTPException(status_code=404, detail="Employees not found")
    logger.info("Read all employee records")
    return db_emp



# ___________Partial update employee__________

@emp.patch("/update_emp_by_patch", response_model=EmployeeBase)
def update_emp_by_patch(employee: EmployeeUpdate, id: str):
    db_emp = db.query(Employee).filter(Employee.id == id, Employee.is_active == True, Employee.is_deleted == False).first()
    if db_emp is None:
        logger.warning(f"Employee not found for update: {id}")
        raise HTTPException(status_code=404, detail="Employee not found")

    for field_name, value in employee.dict().items():
        if value is not None:
            setattr(db_emp, field_name, value)

    db.commit()
    db.refresh(db_emp)
    logger.info(f"Updated employee record: {id}")
    return db_emp



# __________Delete employee____________

@emp.delete("/delete_employee")
def delete_emp(id: str):
    db_emp = db.query(Employee).filter(Employee.id == id, Employee.is_active == True, Employee.is_deleted == False).first()
    if db_emp is None:
        logger.warning(f"Employee not found for deletion: {id}")
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_emp.is_active = False
    db_emp.is_deleted = True
    db.commit()
    logger.info(f"Deleted employee record: {id}")
    return {"message": "Employee deleted successfully"}



# _________Search employee by name____________

@emp.get("/employees_search_by_name", response_model=List[EmployeeBase])
def search_employees_by_name(name: str):
    employees = db.query(Employee).filter(Employee.name == name, Employee.is_active == True, Employee.is_deleted == False).all()
    if not employees:
        logger.warning(f"Employees not found with name: {name}")
        raise HTTPException(status_code=404, detail="Employees not found")
    logger.info(f"Found employees with name: {name}")
    return employees



# ___________Employee salary report____________

@emp.get("/employee_salary_report", response_model=List[EmployeeBase])
def get_employee_salary_report(min_salary: int = 0, max_salary: int = 1000000):
    employees = db.query(Employee).filter(
        Employee.salary >= min_salary,
        Employee.salary <= max_salary,
        Employee.is_active == True,
        Employee.is_deleted == False
    ).all()
    if not employees:
        logger.warning(f"No employees found in salary range: {min_salary} - {max_salary}")
        raise HTTPException(status_code=404, detail="No employees found in this salary range")
    logger.info(f"Found employees in salary range: {min_salary} - {max_salary}")
    return employees



# _____________Get employees by department_____________

@emp.get("/get_employees_by_department", response_model=List[EmployeeBase])
def get_employees_by_department(department: str):
    employees = db.query(Employee).filter(Employee.department == department, Employee.is_active == True, Employee.is_deleted == False).all()
    if not employees:
        logger.warning(f"No employees found in department: {department}")
        raise HTTPException(status_code=404, detail="No employees found in this department")
    logger.info(f"Found employees in department: {department}")
    return employees