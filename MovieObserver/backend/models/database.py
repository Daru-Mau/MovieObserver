from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "movieobserver")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]


def get_database():
    """
    Return the database instance
    """
    return database
