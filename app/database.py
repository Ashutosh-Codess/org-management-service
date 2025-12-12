from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
MASTER_DB = os.getenv("MASTER_DB", "master_db")

client = AsyncIOMotorClient(MONGO_URI)

master_db = client[MASTER_DB]

def get_org_collection(org_name: str):
    return client[f"org_{org_name}"]

