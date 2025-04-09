from fastapi import APIRouter, Form, HTTPException
from app.services.user_service import create_token, db
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await db.usuarios.find_one({"username": username, "password": password})
    if user:
        expire_time = datetime.utcnow() + timedelta(minutes=5)
        token = create_token(username, expires_delta=timedelta(minutes=5))
        return {
            "token_de_sesion": token,
            "duracion": expire_time.isoformat() + "Z"
        }
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")
