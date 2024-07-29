from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.projects import ProjectCreate,updateproject,CompletedProjectsCount
from src.models.projects import Projects
import uuid
from datetime import datetime
from logs.log_config import logger


Project = APIRouter(tags=["Project"])
db = Sessionlocal()



@Project.post("/projects/", response_model=ProjectCreate)
def create_project(project: ProjectCreate):
    logger.info(f"Creating project with title: {project.Title}")
    db_project = Projects(
        id=str(uuid.uuid4()),
        manager_id=project.manager_id,
        emp_id=project.emp_id,
        Title=project.Title,
        Desciption=project.Desciption,
        start_date=project.start_date,
        end_date=project.end_date,
        status=project.status,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    logger.info(f"Project created with ID: {db_project.id}")
    return db_project



@Project.get("/read_Project", response_model=ProjectCreate)
def read_project(id: str):
    logger.info(f"Reading project with ID: {id}")
    project = db.query(Projects).filter(Projects.id == id, Projects.is_active == True, Projects.is_deleted == False).first()
    if project is None:
        logger.error(f"Project with ID {id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    return project



@Project.get("/get_all_Project", response_model=List[ProjectCreate])
def get_all_Project():
    logger.info("Fetching all active and not deleted projects")
    projects = db.query(Projects).filter(Projects.is_active == True, Projects.is_deleted == False).all()
    if not projects:
        logger.error("No projects found")
        raise HTTPException(status_code=404, detail="No projects found")
    return projects



@Project.get("/projects_active", response_model=List[ProjectCreate])
def read_active_projects():
    logger.info("Fetching all active projects")
    active_projects = db.query(Projects).filter(Projects.status == "active", Projects.is_active == True, Projects.is_deleted == False).all()
    if not active_projects:
        logger.error("No active projects found")
        raise HTTPException(status_code=404, detail="No active projects found")
    return active_projects



@Project.get("/projects_complated", response_model=List[ProjectCreate])
def read_complated_projects():
    logger.info("Fetching all completed projects")
    completed_projects = db.query(Projects).filter(Projects.status == "completed", Projects.is_active == True, Projects.is_deleted == False).all()
    if not completed_projects:
        logger.error("No completed projects found")
        raise HTTPException(status_code=404, detail="No completed projects found")
    return completed_projects



@Project.get("/projects_pending", response_model=List[ProjectCreate])
def read_pending_projects():
    logger.info("Fetching all pending projects")
    pending_projects = db.query(Projects).filter(Projects.status == "pending", Projects.is_active == True, Projects.is_deleted == False).all()
    if not pending_projects:
        logger.error("No pending projects found")
        raise HTTPException(status_code=404, detail="No pending projects found")
    return pending_projects



@Project.get("/projects_cancelled", response_model=List[ProjectCreate])
def read_cancelled_projects():
    logger.info("Fetching all cancelled projects")
    cancelled_projects = db.query(Projects).filter(Projects.status == "cancelled", Projects.is_active == True, Projects.is_deleted == False).all()
    if not cancelled_projects:
        logger.error("No cancelled projects found")
        raise HTTPException(status_code=404, detail="No cancelled projects found")
    return cancelled_projects



@Project.patch("/update_project_by_patch", response_model=ProjectCreate)
def update_project_by_patch(id: str, project: updateproject):
    logger.info(f"Updating project with ID: {id}")
    db_project = db.query(Projects).filter(Projects.id == id, Projects.is_active == True, Projects.is_deleted == False).first()
    if db_project is None:
        logger.error(f"Project with ID {id} not found")
        raise HTTPException(status_code=404, detail="Project not found")

    for field_name, value in project.dict().items():
        if value is not None:
            setattr(db_project, field_name, value)
    db.commit()
    db.refresh(db_project)
    logger.info(f"Project with ID {id} updated successfully")
    return db_project



@Project.delete("/delete_Project")
def delete_project(id: str):
    logger.info(f"Deleting project with ID: {id}")
    db_project = db.query(Projects).filter(Projects.id == id, Projects.is_active == True, Projects.is_deleted == False).first()
    if db_project is None:
        logger.error(f"Project with ID {id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.is_active = False
    db_project.is_deleted = True
    db.commit()
    logger.info(f"Project with ID {id} deleted successfully")
    return {"message": "Project deleted successfully"}



@Project.put("/project_complete", response_model=ProjectCreate)
def complete_task(id: str):
    logger.info(f"Completing project with ID: {id}")
    db_project = db.query(Projects).filter(Projects.id == id, Projects.is_active == True, Projects.is_deleted == False).first()
    if db_project is None:
        logger.error(f"Project with ID {id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.status = "completed"
    db_project.end_date = datetime.now()
    db.commit()
    db.refresh(db_project)
    logger.info(f"Project with ID {id} marked as completed")
    return db_project



@Project.get("/projects_manager", response_model=List[ProjectCreate])
def get_projects_by_manager(manager_id: str):
    logger.info(f"Fetching projects for manager ID: {manager_id}")
    db_projects = db.query(Projects).filter(Projects.manager_id == manager_id, Projects.is_active == True, Projects.is_deleted == False).all()
    return db_projects



@Project.get("/projects_employee", response_model=List[ProjectCreate])
def get_projects_by_employee(emp_id: str):
    logger.info(f"Fetching projects for employee ID: {emp_id}")
    db_projects = db.query(Projects).filter(Projects.emp_id == emp_id).all()
    return db_projects



@Project.get("/projects_date_range", response_model=List[ProjectCreate])
def get_projects_by_date_range(start_date: datetime, end_date: datetime):
    logger.info(f"Fetching projects between {start_date} and {end_date}")
    db_projects = db.query(Projects).filter(Projects.start_date >= start_date, Projects.end_date <= end_date).all()
    return db_projects



@Project.get("/projects_count/")
def count_projects(status: str = None, start_date: datetime = None, end_date: datetime = None):
    logger.info(f"Counting projects with status: {status}, between {start_date} and {end_date}")
    query = db.query(Projects)
    
    if status:
        query = query.filter(Projects.status == status)
    if start_date and end_date:
        query = query.filter(Projects.start_date >= start_date, Projects.end_date <= end_date)
    
    count = query.count()
    logger.info(f"Total project count: {count}")
    return {"count": count}



@Project.get("/managers_completed_projects_count", response_model=CompletedProjectsCount)
def get_completed_projects_count(manager_id: str):
    logger.info(f"Fetching completed projects count for manager ID: {manager_id}")
    completed_projects = db.query(Projects).filter(Projects.manager_id == manager_id, Projects.status == "completed").all()
    completed_projects_count = len(completed_projects)
    logger.info(f"Completed projects count for manager ID {manager_id}: {completed_projects_count}")
    return {"completed_projects_count": completed_projects_count}



@Project.get("/projects_overdue", response_model=List[ProjectCreate])
def get_overdue_projects():
    today = datetime.now()
    logger.info(f"Fetching overdue projects as of {today}")
    db_projects = db.query(Projects).filter(
        Projects.end_date < today,
        Projects.status != "completed",
        Projects.is_active == True,
        Projects.is_deleted == False
    ).all()
    return db_projects



@Project.patch("/projects_assign_employee", response_model=ProjectCreate)
def assign_employee_to_project(project_id: str, emp_id: str):
    logger.info(f"Assigning employee ID: {emp_id} to project ID: {project_id}")
    db_project = db.query(Projects).filter(
        Projects.id == project_id,
        Projects.is_active == True,
        Projects.is_deleted == False
    ).first()
    
    if db_project is None:
        logger.error(f"Project with ID {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_project.emp_id = emp_id
    db.commit()
    db.refresh(db_project)
    logger.info(f"Employee ID: {emp_id} assigned to project ID: {project_id}")
    return db_project



@Project.patch("/projects_reopen", response_model=ProjectCreate)
def reopen_project(project_id: str):
    logger.info(f"Reopening project with ID: {project_id}")
    db_project = db.query(Projects).filter(
       Projects.id == project_id,
       Projects.is_active == False,
       Projects.is_deleted == False
    ).first()
    
    if db_project is None:
        logger.error(f"Project with ID {project_id} not found or already active")
        raise HTTPException(status_code=404, detail="Project not found or already active")
    
    db_project.is_active = True
    db_project.status = "in-progress"
    db.commit()
    db.refresh(db_project)
    logger.info(f"Project with ID {project_id} reopened successfully")
    return db_project
