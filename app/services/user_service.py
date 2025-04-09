from fastapi import HTTPException, Header
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from app.db.database import db  # Asegúrate que esto apunta a tu instancia correcta de la DB

# Cargar variables de entorno
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise Exception("La variable de entorno JWT_SECRET no está definida en el archivo .env")


def create_token(username: str, expires_delta: timedelta = timedelta(minutes=5)):
    """Crea un token JWT para el usuario especificado."""
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": username, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str = Header(...)):
    """Verifica la validez de un token JWT pasado como encabezado HTTP."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=403, detail="Token inválido: usuario no encontrado")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
