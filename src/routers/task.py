from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.task import TaskCreate,TaskUpdate
import uuid
from src.models.tasks import Task
from datetime import datetime
from logs.log_config import logger


task = APIRouter(tags=["Tasks"])
db = Sessionlocal()


# _________Create task__________

@task.post("/create_task", response_model=TaskCreate)
def create_task(tasks: TaskCreate):
    db_task = Task(
        id=str(uuid.uuid4()),
        emp_id=tasks.emp_id,
        project_id=tasks.project_id,
        title=tasks.title,
        description=tasks.description,
        status=tasks.status,
        due_date=tasks.due_date
    )

    db.add(db_task)
    db.commit()
    logger.info(f"Created task with ID: {db_task.id}")
    return db_task



# __________Read task_________

@task.get("/read_task", response_model=TaskCreate)
def get_task(task_id: str):
    task = db.query(Task).filter(Task.id == task_id, Task.is_active == True, Task.is_deleted == False).first()
    if task is None:
        logger.warning(f"Task not found for ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Retrieved task with ID: {task_id}")
    return task



# ______Read all tasks______

@task.get("/get_all_tasks", response_model=List[TaskCreate])
def get_all_tasks():
    tasks = db.query(Task).filter(Task.is_active == True, Task.is_deleted == False).all()
    if not tasks:
        logger.warning("No tasks found")
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info("Retrieved all tasks")
    return tasks



# _________Update task by patch_______

@task.patch("/update_task_by_patch", response_model=TaskCreate)
def update_task_by_patch(tasks: TaskUpdate, id: str):
    db_task = db.query(Task).filter(Task.id == id, Task.is_active == True, Task.is_deleted == False).first()

    if db_task is None:
        logger.warning(f"Task not found for ID: {id}")
        raise HTTPException(status_code=404, detail="Task not found")

    for field_name, value in tasks.dict().items():
        if value is not None:
            setattr(db_task, field_name, value)
    
    db.commit()
    logger.info(f"Updated task with ID: {id}")
    return db_task



# __________Delete task__________

@task.delete("/delete_task")
def delete_task(id: str):
    db_task = db.query(Task).filter(Task.id == id, Task.is_active == True, Task.is_deleted == False).first()
    if db_task is None:
        logger.warning(f"Task not found for ID: {id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.is_active = False
    db_task.is_deleted = True
    db.commit()
    logger.info(f"Deleted task with ID: {id}")
    return {"message": "Task deleted successfully"}



# _________Get tasks by project id____________

@task.get("/projects_tasks", response_model=List[TaskCreate])
def get_tasks_by_project(project_id: str):
    db_tasks = db.query(Task).filter(Task.project_id == project_id, Task.is_active == True, Task.is_deleted == False).all()
    if not db_tasks:
        logger.warning(f"No tasks found for project ID: {project_id}")
        raise HTTPException(status_code=404, detail="No tasks found for this project")
    logger.info(f"Retrieved tasks for project ID: {project_id}")
    return db_tasks



# _________Get tasks by employee________

@task.get("/employees_tasks", response_model=List[TaskCreate])
def get_tasks_by_employee(emp_id: str):
    db_tasks = db.query(Task).filter(Task.emp_id == emp_id, Task.is_active == True, Task.is_deleted == False).all()
    if not db_tasks:
        logger.warning(f"No tasks found for employee ID: {emp_id}")
        raise HTTPException(status_code=404, detail="No tasks found for this employee")
    logger.info(f"Retrieved tasks for employee ID: {emp_id}")
    return db_tasks



# _____Retrieve not completed tasks______

@task.get("/tasks_overdue", response_model=List[TaskCreate])
def get_overdue_tasks():
    today = datetime.now()
    db_tasks = db.query(Task).filter(
        Task.due_date < today,
        Task.status != "completed",
        Task.is_active == True,
        Task.is_deleted == False
    ).all()
    logger.info("Retrieved overdue tasks")
    return db_tasks



# _________Reopen a task that was marked as completed or inactive________

@task.patch("/tasks_reopen", response_model=TaskCreate)
def reopen_task(task_id: str):
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.is_active == False,
        Task.is_deleted == False
    ).first()
    
    if db_task is None:
        logger.warning(f"Task not found or already active for ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found or already active")
    
    db_task.is_active = True
    db_task.status = "todo"
    db.commit()
    db.refresh(db_task)
    logger.info(f"Reopened task with ID: {task_id}")
    return db_task



# _______Assign a task to a specific employee_________

@task.patch("/tasks_assign", response_model=TaskCreate)
def assign_task(task_id: str, emp_id: str):
    db_task = db.query(Task).filter(Task.id == task_id, Task.is_active == True, Task.is_deleted == False).first()
    
    if db_task is None:
        logger.warning(f"Task not found for ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.emp_id = emp_id
    db.commit()
    db.refresh(db_task)
    logger.info(f"Assigned employee ID: {emp_id} to task ID: {task_id}")
    return db_task



# ________Mark task as completed__________

@task.patch("/tasks_complete", response_model=TaskCreate)
def complete_task(task_id: str):
    db_task = db.query(Task).filter(Task.id == task_id, Task.is_active == True, Task.is_deleted == False).first()
    
    if db_task is None:
        logger.warning(f"Task not found for ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.status = "completed"
    db_task.is_active = False
    db.commit()
    db.refresh(db_task)
    logger.info(f"Marked task with ID: {task_id} as completed")
    return db_task



# ___________Get tasks by employee and status_______

@task.get("/employees_tasks_status", response_model=List[TaskCreate])
def get_tasks_by_employee_and_status(emp_id: str, status: str):
    query = db.query(Task).filter(Task.emp_id == emp_id, Task.is_active == True, Task.is_deleted == False)
    
    if status:
        query = query.filter(Task.status == status)
    
    db_tasks = query.all()
    
    if not db_tasks:
        logger.warning(f"No tasks found for employee ID: {emp_id} with status: {status}")
        raise HTTPException(status_code=404, detail="No tasks found for this employee")
    
    logger.info(f"Retrieved tasks for employee ID: {emp_id} with status: {status}")
    return db_tasks