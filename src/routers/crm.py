from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from typing import List
from src.schemas.crm import CustomerBase,updatecustomer
from src.models.crm import Customer
from datetime import datetime
from logs.log_config import logger


crm = APIRouter(tags=["CRM"])
db = Sessionlocal()



# __________Create customer____________

@crm.post("/create_customer", response_model=CustomerBase)
def create_customer(customer_data: CustomerBase):
   
    if db.query(Customer).filter(Customer.email == customer_data.email).first():
        logger.warning(f"Attempt to register an already registered email: {customer_data.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    db_customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        phone_number=customer_data.phone_number,
        address=customer_data.address,
        industry=customer_data.industry,
    )
    db.add(db_customer)
    db.commit()
    logger.info(f"Created new customer: {customer_data.email}")
    return db_customer


# ________Read customer_____________

@crm.get("/read_customer", response_model=CustomerBase)
def read_customer(customer_id: str):
   
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True, Customer.is_deleted == False).first()
    if customer is None:
        logger.warning(f"Customer not found: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    logger.info(f"Read customer record: {customer_id}")
    return customer



# __________Update customer___________

@crm.patch("/update_customer", response_model=CustomerBase)
def update_customer(customer_id: str, customer: updatecustomer):
  
    db_customer = db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True, Customer.is_deleted == False).first()
    if db_customer is None:
        logger.warning(f"Customer not found for update: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    
    db_customer.updated_at = datetime.now()
    db.commit()
    db.refresh(db_customer)
    logger.info(f"Updated customer record: {customer_id}")
    return db_customer



# _______Delete customer______________

@crm.delete("/delete_customer", response_model=CustomerBase)
def delete_customer(customer_id: str):
   
    db_customer = db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True, Customer.is_deleted == False).first()
    if db_customer is None:
        logger.warning(f"Customer not found for deletion: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    logger.info(f"Deleted customer record: {customer_id}")
    return db_customer



# _________Count active customers____________

@crm.get("/customers_active_count", response_model=int)
def count_active_customers():
    
    count = db.query(Customer).filter(Customer.is_active == True).count()
    logger.info("Counted active customers")
    return count