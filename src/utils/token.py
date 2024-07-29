from datetime import datetime,timedelta
from fastapi import HTTPException,status,Security
from dotenv import load_dotenv
import os
from jose import JWTError,jwt

from datetime import datetime,timedelta
from fastapi import HTTPException,status,Security
from dotenv import load_dotenv
import os
from jose import JWTError,jwt
load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))

#payload

def get_token(id):
    payload = {
        "user_id": id,
        "exp": datetime.now() + timedelta(minutes=15),
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(type(access_token))
    return access_token

#decode id

def decode_token_user_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid token",)
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid token",)