from fastapi import FastAPI
from src.routers.user import users
from src.routers.employee import emp
from src.routers.manager import Managers
from src.routers.projects import Project
from src.routers.task import task
from src.routers.TimeTracking import Timetracking
from src.routers.equipment import equipment
from src.routers.crm import crm
from src.routers.event import events 
from src.routers.attendence import  Attendences
from src.routers.JobOpening import jobopening
from src.routers.EmployeeExit import empexit
from src.routers.notification import notifications

app =FastAPI(title = "IT company resource management")
app.include_router(users)
app.include_router(emp)
app.include_router(Managers)
app.include_router(Project)
app.include_router(task)
app.include_router(Timetracking)
app.include_router(equipment)
app.include_router(crm)
app.include_router(events)
app.include_router(Attendences)
app.include_router(jobopening)
app.include_router(empexit)
app.include_router(notifications)