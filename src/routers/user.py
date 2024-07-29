from fastapi import FastAPI, HTTPException, APIRouter,Depends,Header
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.user import userschema,updateuser
from src.models.user import User
from src.models.otp import OTPS
from src.schemas.otp import OTPRequest, OTPVerificationRequest
from src.utils.token import decode_token_user_id,get_token
import random
from datetime import datetime, timedelta
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logs.log_config import logger
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


users = APIRouter(tags=["User"])
db = Sessionlocal()



# __________Create user___________

@users.post("/create_user", response_model=userschema)
def create_user(user: userschema):
    logger.info(f"Creating user with username: {user.username} and email: {user.email}")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=pwd_context.hash(user.password),
        role=user.role,
        last_login=user.last_login,
        phone_number=user.phone_number
    )
    db.add(new_user)
    db.commit()
    logger.info(f"User created with ID: {new_user.id}")
    
    return new_user



# ___________Generate OTP___________

def generate_otp(email: str):
    otp_code = str(random.randint(100000, 999999))
    expiration_time = datetime.now() + timedelta(minutes=10)

    otp = OTPS(
        id=str(uuid.uuid4()),
        user_email=email,
        otp=otp_code,
        expiration_time=expiration_time
    )
    db.add(otp)
    db.commit()
    logger.info(f"Generated OTP for email: {email}")
    
    return otp_code

# Send OTP email
def send_otp_email(email: str, otp_code: str):
    sender_email = "your_email@example.com"  # Replace with your email
    receiver_email = email
    password = "your_password"  # Replace with your email password
    subject = "Your OTP Code"
    message_text = f"Your OTP is {otp_code} which is valid for 10 minutes"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        logger.info(f"OTP email sent to {receiver_email}")
        server.quit()
    except Exception as e:
        logger.error(f"Failed to send email: {e}")



# ____________Generate OTP endpoint___________

@users.post("/generate_otp")
def generate_otp_endpoint(request: OTPRequest):
    logger.info(f"Generating OTP for email: {request.email}")
    user_email = request.email
    user_info = db.query(User).filter(User.email == user_email, User.is_active == True, User.is_deleted == False).first()

    if not user_info:
        logger.error(f"Invalid or missing email address: {user_email}")
        raise HTTPException(status_code=400, detail="Invalid or missing email address")

    otp_code = generate_otp(user_email)
    send_otp_email(user_email, otp_code)
    return {"message": "OTP generated and sent successfully to the provided email address."}


# _______Verify OTP endpoint____________

@users.post("/verify_otp")
def verify_otp_endpoint(request: OTPVerificationRequest):
    logger.info(f"Verifying OTP for email: {request.email}")
    email = request.email
    entered_otp = request.otp

    stored_otp = db.query(OTPS).filter(OTPS.user_email == email, OTPS.is_active == True).first()

    if stored_otp:
        if datetime.now() < stored_otp.expiration_time:
            if entered_otp == stored_otp.otp:
                stored_otp.is_active = False
                stored_otp.is_deleted = True
                db.commit()

                user = db.query(User).filter(User.email == email, User.is_active == True, User.is_deleted == False).first()
                if user:
                    user.is_verified = True
                    db.commit()
                    logger.info(f"OTP verification successful for email: {email}")
                    return {"message": "OTP verification successful"}

                logger.error(f"User is not verified: {email}")
                return {"error": "User is not verified"}
            else:
                logger.error(f"Incorrect OTP entered for email: {email}")
                return {"error": "Incorrect OTP entered"}
        else:
            db.delete(stored_otp)
            db.commit()
            logger.error(f"OTP has expired for email: {email}")
            return {"error": "OTP has expired"}
    else:
        logger.error(f"No OTP found for email: {email}")
        return {"error": "No OTP found"}


# _________Logging in__________

@users.get("/logging")
def logging(uname: str, password: str):
    logger.info(f"User login attempt for username: {uname}")
    db_user = db.query(User).filter(User.username == uname, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()

    if db_user is None:
        logger.error(f"User not found: {uname}")
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password, db_user.password):
        logger.error(f"Incorrect password for username: {uname}")
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = get_token(db_user.id)
    logger.info(f"User logged in successfully: {uname}")
    return access_token


# ________Get user by token_________

@users.get("/get_user_by_token", response_model=userschema)
def read_user(token: str = Header(...)):
    logger.info(f"Fetching user by token")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()

    if db_user is None:
        logger.error(f"User not found with token: {token}")
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


# _________Get all users______

@users.get("/get_all_user", response_model=List[userschema])
def read_all_user():
    logger.info("Fetching all users")
    db_user = db.query(User).filter(User.is_active == True, User.is_verified == True, User.is_deleted == False).all()
    
    if not db_user:
        logger.error("No users found")
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user



# ____________Update user by put_____________

@users.put("/update_user_by_put", response_model=userschema)
def update_user(usern: userschema, token: str = Header(...)):
    logger.info(f"Updating user details for token: {token}")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()
    
    if db_user is None:
        logger.error(f"User not found with token: {token}")
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.is_verified:
        logger.error(f"User is not verified with token: {token}")
        return "User not verified"
    
    db_user.username = usern.username
    db_user.email = usern.email
    db_user.password = pwd_context.hash(usern.password)
    db_user.role = usern.role
    db_user.last_login = usern.last_login
    db_user.phone_number = usern.phone_number

    db.commit()
    logger.info(f"User updated successfully with ID: {user_id}")
    return db_user


# ___________Delete user___________

@users.delete("/delete_user_by_token")
def delete_user(token: str = Header(...)):
    logger.info(f"Deleting user with token: {token}")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()

    if db_user is None:
        logger.error(f"User not found with token: {token}")
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.is_verified:
        logger.error(f"User is not verified with token: {token}")
        return "User not verified"

    db_user.is_active = False
    db_user.is_deleted = True
    db.commit()
    logger.info(f"User deleted successfully with ID: {user_id}")
    return {"message": "User deleted successfully"}


# _____________Forget password__________

@users.put("/forget_password")
def forget_password(user_newpass: str, token: str = Header(...)):
    logger.info(f"Processing password reset for token: {token}")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()

    if db_user is None:
        logger.error(f"User not found with token: {token}")
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.is_verified:
        logger.error(f"User is not verified with token: {token}")
        return "User not verified"

    db_user.password = pwd_context.hash(user_newpass)
    db.commit()
    logger.info(f"Password reset successfully for user with ID: {user_id}")
    return "Password reset successfully"


# ___________Reset password__________

@users.put("/reset_password")
def reset_password_by_token(old_password: str, new_password: str, token: str = Header(...)):
    logger.info(f"Processing password reset by token for token: {token}")
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True, User.is_verified == True, User.is_deleted == False).first()

    if db_user is None:
        logger.error(f"User not found with token: {token}")
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.is_verified:
        logger.error(f"User is not verified with token: {token}")
        return "User not verified"

    if pwd_context.verify(old_password, db_user.password):
        db_user.password = pwd_context.hash(new_password)
        db.commit()
        logger.info(f"Password reset successfully for user with ID: {user_id}")
        return {"message": "Password reset successfully"}
    else:
        logger.error(f"Old password does not match for user with ID: {user_id}")
        return "Old password is not matched"