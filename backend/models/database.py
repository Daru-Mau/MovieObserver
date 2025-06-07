from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "movieobserver")

# In-memory mock database for development
mock_db = {
    "movies": [],
    "theaters": []
}


class MockCollection:
    def __init__(self, data: list):
        self.data = data

    async def find(self, query=None):
        return self

    async def to_list(self, length: int):
        return self.data

    async def find_one(self, query):
        # Simple query matching for _id
        if query and "_id" in query:
            return next((item for item in self.data if item.get("_id") == query["_id"]), None)
        return self.data[0] if self.data else None

    async def insert_one(self, document):
        self.data.append(document)

    async def insert_many(self, documents):
        self.data.extend(documents)


class MockDatabase:
    def __init__(self, collections: Dict[str, list]):
        self.collections = {name: MockCollection(
            data) for name, data in collections.items()}

    def __getitem__(self, name: str) -> MockCollection:
        if name not in self.collections:
            self.collections[name] = MockCollection([])
        return self.collections[name]


try:
    # Try to connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    # Verify the connection
    client.server_info()
    database = client[DB_NAME]
    logging.info("Connected to MongoDB successfully")
except Exception as e:
    logging.warning(
        f"Could not connect to MongoDB: {e}. Using mock database instead.")
    database = MockDatabase(mock_db)


def get_database():
    """
    Return the database instance (either MongoDB or mock)
    """
    return database
