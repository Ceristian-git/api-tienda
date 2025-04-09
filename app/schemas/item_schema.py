from typing import List
from pydantic import BaseModel, Field

class PCModel(BaseModel):
    nombre: str = Field(..., example="PC Gamer")
    componentes: List[str] = Field(..., example=["Intel i7", "RTX 3060", "16GB RAM"])
    precio: float = Field(..., example=3500000)
    categoria: str = Field(..., example="gaming")

class RecomendacionInput(BaseModel):
    presupuesto: float
    objetivo: str
