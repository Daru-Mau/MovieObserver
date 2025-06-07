"""
This module is maintained for backwards compatibility.
The project now uses Supabase for database operations.
See models/supabase.py for the current database implementation.
"""
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Load environment variables
load_dotenv()

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


# Initialize mock database
database = MockDatabase(mock_db)
logging.info("Using mock database for legacy code support")


def get_database():
    """
    Return the mock database instance
    Note: This function is maintained for backwards compatibility
    """
    return database
