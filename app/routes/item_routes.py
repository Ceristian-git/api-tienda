from fastapi import APIRouter, HTTPException, Body, Depends
from app.schemas.item_schema import PCModel, RecomendacionInput
from app.services.item_service import (
    get_all_pcs, get_pc_by_id, create_pc, update_pc, delete_pc, recomendar_pc
)
from app.services.user_service import verify_token

router = APIRouter()

@router.get("/")
async def get_all():
    return await get_all_pcs()

@router.get("/{pc_id}")
async def get_one(pc_id: int):
    return await get_pc_by_id(pc_id)

@router.post("/")
async def create(pc: PCModel):
    return await create_pc(pc)

@router.put("/{pc_id}")
async def update(pc_id: int, pc: PCModel = Body(...)):
    return await update_pc(pc_id, pc)

@router.delete("/{pc_id}")
async def delete(pc_id: int):
    return await delete_pc(pc_id)

@router.post("/recomendar")
async def recomendar(data: RecomendacionInput, auth: bool = Depends(verify_token)):
    return await recomendar_pc(data)
