from fastapi import FastAPI, HTTPException, Body, Depends, Form
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.database import db, get_next_id
from app.models import PCModel
from app.chat import obtener_recomendacion_chatgpt
from app.auth import verify_token, create_token

class RecomendacionInput(BaseModel):
    presupuesto: float
    objetivo: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API de Tienda de PCs"}

@app.get("/pcs")
async def get_all_pcs():
    pcs = []
    async for pc in db.pcs.find():
        pcs.append(pc)
    return pcs

@app.get("/pcs/{pc_id}")
async def get_pc(pc_id: int):
    pc = await db.pcs.find_one({"_id": pc_id})
    if pc:
        return pc
    raise HTTPException(status_code=404, detail="PC no encontrada")

@app.post("/pcs")
async def create_pc(pc: PCModel):
    pc_data = pc.dict()
    pc_data["_id"] = await get_next_id()
    await db.pcs.insert_one(pc_data)
    return {"id": pc_data["_id"]}

@app.put("/pcs/{pc_id}")
async def update_pc(pc_id: int, pc: PCModel = Body(...)):
    result = await db.pcs.update_one(
        {"_id": pc_id},
        {"$set": pc.dict()}
    )
    if result.modified_count:
        return {"message": "PC actualizada"}
    raise HTTPException(status_code=404, detail="PC no encontrada o sin cambios")

@app.delete("/pcs/{pc_id}")
async def delete_pc(pc_id: int):
    result = await db.pcs.delete_one({"_id": pc_id})
    if result.deleted_count:
        return {"message": "PC eliminada"}
    raise HTTPException(status_code=404, detail="PC no encontrada")

@app.post("/recomendar/")
async def recomendar_pc(data: RecomendacionInput, auth: bool = Depends(verify_token)):
    recomendacion = await obtener_recomendacion_chatgpt(data.presupuesto, data.objetivo)
    return {"respuesta": recomendacion}

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await db.usuarios.find_one({"username": username, "password": password})
    if user:
        expire_time = datetime.utcnow() + timedelta(minutes=5)
        token = create_token(username, expires_delta=timedelta(minutes=5))
        return {
            "token_de_sesion": token,
            "duracion": expire_time.isoformat() + "Z"
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
