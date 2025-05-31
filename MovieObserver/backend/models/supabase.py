from supabase import create_client, Client
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
_client: Optional[Client] = None


def get_client() -> Client:
    """
    Get or create Supabase client instance
    Returns:
        Client: Supabase client instance
    """
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# SQL for creating tables
CREATE_MOVIES_TABLE = """
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    original_title TEXT,
    date DATE NOT NULL,
    image_url TEXT,
    description TEXT,
    duration INTEGER,
    genres TEXT[],
    rating FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

CREATE_SHOWTIMES_TABLE = """
CREATE TABLE IF NOT EXISTS showtimes (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    time TIME NOT NULL,
    theater TEXT NOT NULL,
    room TEXT,
    is_original_language BOOLEAN DEFAULT false,
    is_3d BOOLEAN DEFAULT false,
    booking_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

CREATE_THEATERS_TABLE = """
CREATE TABLE IF NOT EXISTS theaters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT NOT NULL,
    website TEXT,
    phone TEXT,
    features TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""


async def init_database():
    """Initialize database tables"""
    client = get_client()

    try:
        # Test connection by accessing movies table
        response = client.table('movies').select('id').limit(1).execute()
        print("Database tables already exist")
    except Exception as e:
        print(f"Error accessing tables: {e}")
        print("Creating tables via Supabase dashboard is required.")
        print("Please copy the following SQL and run it in the Supabase SQL editor:")
        print("\n--- SQL to create tables ---")
        print(CREATE_MOVIES_TABLE)
        print(CREATE_SHOWTIMES_TABLE)
        print(CREATE_THEATERS_TABLE)
        print("----------------------------")
