import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

env_path = os.path.abspath('.env')
load_dotenv(env_path)

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise Exception('MONGO_URI not set')

client = AsyncIOMotorClient(MONGO_URI)
master_db = client['master_db']
