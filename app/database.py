from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URI)
db = client.pc_store

# Generador de ID consecutivo
async def get_next_id():
    counter = await db.counters.find_one_and_update(
        {"_id": "pc_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]
