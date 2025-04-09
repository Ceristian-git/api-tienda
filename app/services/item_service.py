from fastapi import HTTPException
from app.db.database import db, get_next_id
from app.schemas.item_schema import PCModel
from app.services.chat_service import obtener_recomendacion_chatgpt

async def get_all_pcs():
    pcs = []
    async for pc in db.pcs.find():
        pcs.append(pc)
    return pcs

async def get_pc_by_id(pc_id: int):
    pc = await db.pcs.find_one({"_id": pc_id})
    if pc:
        return pc
    raise HTTPException(status_code=404, detail="PC no encontrada")

async def create_pc(pc: PCModel):
    pc_data = pc.dict()
    pc_data["_id"] = await get_next_id()
    await db.pcs.insert_one(pc_data)
    return {"id": pc_data["_id"]}

async def update_pc(pc_id: int, pc: PCModel):
    result = await db.pcs.update_one({"_id": pc_id}, {"$set": pc.dict()})
    if result.modified_count:
        return {"message": "PC actualizada"}
    raise HTTPException(status_code=404, detail="PC no encontrada o sin cambios")

async def delete_pc(pc_id: int):
    result = await db.pcs.delete_one({"_id": pc_id})
    if result.deleted_count:
        return {"message": "PC eliminada"}
    raise HTTPException(status_code=404, detail="PC no encontrada")

async def recomendar_pc(data):
    return {
        "respuesta": await obtener_recomendacion_chatgpt(data.presupuesto, data.objetivo)
    }
