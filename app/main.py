from fastapi import FastAPI
from app.routes import item_routes, user_routes

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API de Tienda de PCs"}

app.include_router(item_routes.router, prefix="/pcs", tags=["PCs"])
app.include_router(user_routes.router, tags=["Usuarios"])
