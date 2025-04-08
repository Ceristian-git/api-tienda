from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def create_token(username: str, expires_delta: timedelta = timedelta(minutes=5)):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": username, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=403, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
