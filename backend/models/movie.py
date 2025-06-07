from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Showtime(BaseModel):
    time: str
    theater: str
    room: str
    is_original_language: bool
    is_3d: bool = False
    booking_url: Optional[str] = None


class Movie(BaseModel):
    title: str
    original_title: Optional[str] = None
    date: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None  # In minutes
    genres: Optional[List[str]] = None
    rating: Optional[float] = None
    showtimes: List[Showtime]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
