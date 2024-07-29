from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.equipement import EquipmentBase,UpdateEquipment
from src.models.equipment import Equipment
from typing import List
from logs.log_config import logger


equipment = APIRouter(tags=["Equipment"])
db = Sessionlocal()


@equipment.post("/create_equipment/", response_model=EquipmentBase)
def create_equipment(equipment: EquipmentBase):
    logger.info(f"Creating equipment: {equipment}")
    
    db_equipment = Equipment(
        name=equipment.name,
        type=equipment.type,
        purchase_date=equipment.purchase_date,
        status=equipment.status,
        assigned_to=equipment.assigned_to,
        value=equipment.value
    )
    db.add(db_equipment)
    db.commit()
    
    logger.info(f"Equipment created with ID: {db_equipment.id}")
    return db_equipment



@equipment.get("/read_equipment", response_model=EquipmentBase)
def read_equipment(id: str):
    logger.info(f"Reading equipment with ID: {id}")
    
    equipment = db.query(Equipment).filter(Equipment.id == id).first()
    if equipment is None:
        logger.error(f"Equipment with ID {id} not found")
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    logger.info(f"Equipment found: {equipment}")
    return equipment



@equipment.get("/list_of_equipment", response_model=List[EquipmentBase])
def list_of_equipment():
    logger.info("Listing all active and not deleted equipment")
    
    equipment_list = db.query(Equipment).filter(Equipment.is_active == True, Equipment.is_deleted == False).all()
    
    logger.info(f"Number of equipment items listed: {len(equipment_list)}")
    return equipment_list



@equipment.patch("/update_equipment", response_model=EquipmentBase)
def update_equipment(equipment_id: str, equipment: UpdateEquipment):
    logger.info(f"Updating equipment with ID: {equipment_id} with data: {equipment.dict()}")
    
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if db_equipment is None:
        logger.error(f"Equipment with ID {equipment_id} not found")
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for field, value in equipment.dict(exclude_unset=True).items():
        setattr(db_equipment, field, value)
    
    db.commit()
    logger.info(f"Equipment with ID {equipment_id} updated")
    return db_equipment



@equipment.delete("/delete_equipment", response_model=EquipmentBase)
def delete_equipment(equipment_id: str):
    logger.info(f"Deleting equipment with ID: {equipment_id}")
    
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if db_equipment is None:
        logger.error(f"Equipment with ID {equipment_id} not found")
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db_equipment.is_active = False
    db_equipment.is_deleted = True
    db.commit()
    
    logger.info(f"Equipment with ID {equipment_id} deleted")
    return db_equipment



@equipment.put("/equipment_allocate")
def allocate_equipment(equipment_id: str, employee_id: str):
    logger.info(f"Allocating equipment with ID: {equipment_id} to employee with ID: {employee_id}")
    
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        logger.error(f"Equipment with ID {equipment_id} not found")
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    if equipment.status != "available":
        logger.error(f"Equipment with ID {equipment_id} is not available for allocation")
        raise HTTPException(status_code=400, detail="Equipment is not available for allocation")
    
    equipment.status = "in use"
    equipment.assigned_to = employee_id
    db.commit()
    
    logger.info(f"Equipment with ID {equipment_id} allocated to employee with ID: {employee_id}")
    return {"message": f"Equipment {equipment_id} allocated to employee {employee_id}"}



@equipment.put("/equipment_release")
def release_equipment(equipment_id: str):
    logger.info(f"Releasing equipment with ID: {equipment_id}")
    
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        logger.error(f"Equipment with ID {equipment_id} not found")
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    equipment.status = "available"
    equipment.assigned_to = None
    db.commit()
    
    logger.info(f"Equipment with ID {equipment_id} released")
    return {"message": f"Equipment {equipment_id} released"}



@equipment.patch("/equipment_unassign", response_model=EquipmentBase)
def unassign_equipment_from_employee(equipment_id: str):
    logger.info(f"Unassigning equipment with ID: {equipment_id}")
    
    db_equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id,
        Equipment.is_deleted == False
    ).first()

    if db_equipment is None:
        logger.error(f"Equipment with ID {equipment_id} not found")
        raise HTTPException(status_code=404, detail="Equipment not found")

    db_equipment.assigned_to = None
    db.commit()
    db.refresh(db_equipment)
    
    logger.info(f"Equipment with ID {equipment_id} unassigned")
    return db_equipment



@equipment.get("/equipment_usage", response_model=dict)
def get_equipment_usage_statistics():
    logger.info("Getting equipment usage statistics")
    
    total_equipment = db.query(Equipment).filter(Equipment.is_deleted == False).count()
    assigned_equipment = db.query(Equipment).filter(Equipment.assigned_to.isnot(None), Equipment.is_deleted == False).count()
    
    statistics = {
        "total_equipment": total_equipment,
        "assigned_equipment": assigned_equipment,
        "unassigned_equipment": total_equipment - assigned_equipment
    }
    
    logger.info(f"Equipment usage statistics: {statistics}")
    return statistics