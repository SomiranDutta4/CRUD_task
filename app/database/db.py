from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

client = AsyncIOMotorClient(
    os.getenv("MONGO_URL"),
    tlsCAFile=certifi.where()
)

db = client["crud_task"]