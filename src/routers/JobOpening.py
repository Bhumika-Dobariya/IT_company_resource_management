from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.jobopening import JobOpeningBase,UpdateJobopening
from src.models.jobopening import JobOpening
import uuid
from datetime import datetime
from logs.log_config import logger


jobopening = APIRouter(tags=["jobopening"])
db = Sessionlocal()


# _______________Create Job Opening______________

@jobopening.post("/job_openings/", response_model=JobOpeningBase)
def create_job_opening(job_opening: JobOpeningBase):
    logger.info(f"Creating job opening with data: {job_opening}")
    
    db_job_opening = JobOpening(
        id=str(uuid.uuid4()),
        title=job_opening.title,
        description=job_opening.description,
        department=job_opening.department,
        location=job_opening.location,
        experience_required=job_opening.experience_required,
        education_required=job_opening.education_required,
        salary_range=job_opening.salary_range,
        is_open=True,
    )
    db.add(db_job_opening)
    db.commit()
    db.refresh(db_job_opening)
    
    logger.info(f"Job opening created with ID: {db_job_opening.id}")
    return db_job_opening



# _______________Read Job Opening by ID______________

@jobopening.get("/get_job_openings", response_model=JobOpeningBase)
def read_job_opening(job_id: str):
    logger.info(f"Reading job opening with ID: {job_id}")
    
    job_opening = db.query(JobOpening).filter(JobOpening.id == job_id).first()
    if job_opening is None:
        logger.error(f"Job opening with ID {job_id} not found")
        raise HTTPException(status_code=404, detail="Job opening not found")
    
    logger.info(f"Job opening found: {job_opening}")
    return job_opening



# _______________List All Job Openings______________

@jobopening.get("/list_of_job_openings", response_model=List[JobOpeningBase])
def list_job_openings():
    logger.info("Listing all job openings")
    
    job_openings = db.query(JobOpening).all()
    
    logger.info(f"Number of job openings listed: {len(job_openings)}")
    return job_openings



# _______________Update Job Opening by ID______________

@jobopening.patch("/update_job_openings", response_model=JobOpeningBase)
def update_job_opening(job_id: str, job_opening_update: UpdateJobopening):
    logger.info(f"Updating job opening with ID: {job_id} with data: {job_opening_update.dict()}")
    
    job_opening = db.query(JobOpening).filter(JobOpening.id == job_id).first()
    if job_opening is None:
        logger.error(f"Job opening with ID {job_id} not found")
        raise HTTPException(status_code=404, detail="Job opening not found")

    update_data = job_opening_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job_opening, key, value)

    db.commit()
    db.refresh(job_opening)
    
    logger.info(f"Job opening with ID {job_id} updated")
    return job_opening



# _______________Delete Job Opening by ID______________

@jobopening.delete("/delete_job_openings", response_model=JobOpeningBase)
def delete_job_opening(job_id: str):
    logger.info(f"Deleting job opening with ID: {job_id}")
    
    job_opening = db.query(JobOpening).filter(JobOpening.id == job_id).first()
    if job_opening is None:
        logger.error(f"Job opening with ID {job_id} not found")
        raise HTTPException(status_code=404, detail="Job opening not found")
    
    db.delete(job_opening)
    db.commit()
    
    logger.info(f"Job opening with ID {job_id} deleted")
    return job_opening



# _______________Close Job Opening by ID______________

@jobopening.patch("/job_openings_close", response_model=JobOpeningBase)
async def close_job_opening(job_opening_id: str):
    logger.info(f"Closing job opening with ID: {job_opening_id}")
    
    db_job_opening = db.query(JobOpening).filter(JobOpening.id == job_opening_id).first()
    if db_job_opening is None:
        logger.error(f"Job opening with ID {job_opening_id} not found")
        raise HTTPException(status_code=404, detail="Job opening not found")
    
    db_job_opening.is_open = False
    db_job_opening.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_job_opening)
    
    logger.info(f"Job opening with ID {job_opening_id} closed")
    return db_job_opening



# _______________Get All Open Job Openings______________

@jobopening.get("/job_openings_open", response_model=List[JobOpeningBase])
async def read_open_job_openings():
    logger.info("Fetching all open job openings")
    
    job_openings = db.query(JobOpening).filter(JobOpening.is_open == True).all()
    
    logger.info(f"Number of open job openings found: {len(job_openings)}")
    return job_openings



# _______________Get All Closed Job Openings______________

@jobopening.get("/job_openings_closed/", response_model=List[JobOpeningBase])
async def read_closed_job_openings():
    logger.info("Fetching all closed job openings")
    
    job_openings = db.query(JobOpening).filter(JobOpening.is_open == False).all()
    
    logger.info(f"Number of closed job openings found: {len(job_openings)}")
    return job_openings



# _______________Get Job Openings by Location______________

@jobopening.get("/job_openings_location", response_model=List[JobOpeningBase])
async def read_job_openings_by_location(location: str):
    logger.info(f"Fetching job openings at location: {location}")
    
    job_openings = db.query(JobOpening).filter(JobOpening.location == location).all()
    
    logger.info(f"Number of job openings found at location {location}: {len(job_openings)}")
    return job_openings



# _______________Reopen Job Opening by ID______________

@jobopening.patch("/job_openings_reopen", response_model=JobOpeningBase)
async def reopen_job_opening(job_opening_id: str):
    logger.info(f"Reopening job opening with ID: {job_opening_id}")
    
    db_job_opening = db.query(JobOpening).filter(JobOpening.id == job_opening_id).first()
    if db_job_opening is None:
        logger.error(f"Job opening with ID {job_opening_id} not found")
        raise HTTPException(status_code=404, detail="Job opening not found")
    
    db_job_opening.is_open = True
    db_job_opening.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_job_opening)
    
    logger.info(f"Job opening with ID {job_opening_id} reopened")
    return db_job_opening