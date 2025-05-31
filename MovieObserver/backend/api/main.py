from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime, timedelta

# Import database and models
from models.database import get_database
from models.movie import Movie
from scraper.scraper_service import ScraperService

app = FastAPI(title="Movie Observer API",
              description="API for retrieving movie showtimes and language information",
              version="1.0.0")

# Setup CORS to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to MovieObserver API"}


@app.get("/movies")
async def get_all_movies():
    """Get all movies from database"""
    try:
        db = get_database()
        movies = await db["movies"].find().to_list(1000)
        return movies
    except Exception as e:
        # If database is not available, return sample data
        return []


@app.get("/movies/{date}")
async def get_movies_by_date(date: str):
    # Sample data for testing - in production this would query the database
    sample_movies = [
        {
            "title": "Dune: Part Two",
            "original_title": "Dune: Part Two",
            "date": date,
            "image_url": "https://example.com/dune2.jpg",
            "description": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
            "duration": 166,
            "genres": ["Sci-Fi", "Adventure", "Drama"],
            "rating": 8.5,
            "showtimes": [
                {
                    "time": "14:00",
                    "theater": "Grand Cinema City",
                    "room": "Screen 1",
                    "is_original_language": True,
                    "is_3d": False,
                    "booking_url": "https://example.com/book/1"
                },
                {
                    "time": "17:30",
                    "theater": "Grand Cinema City", 
                    "room": "Screen 2",
                    "is_original_language": False,
                    "is_3d": True,
                    "booking_url": "https://example.com/book/2"
                },
                {
                    "time": "20:45",
                    "theater": "Arthouse Pavilion",
                    "room": "Main Hall",
                    "is_original_language": True,
                    "is_3d": False,
                    "booking_url": "https://example.com/book/3"
                }
            ]
        },
        {
            "title": "Oppenheimer",
            "original_title": "Oppenheimer", 
            "date": date,
            "image_url": "https://example.com/oppenheimer.jpg",
            "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.",
            "duration": 180,
            "genres": ["Biography", "Drama", "History"],
            "rating": 8.3,
            "showtimes": [
                {
                    "time": "15:30",
                    "theater": "Film Forum",
                    "room": "Screen A",
                    "is_original_language": True,
                    "is_3d": False,
                    "booking_url": "https://example.com/book/4"
                },
                {
                    "time": "19:00",
                    "theater": "Megaplex 20",
                    "room": "IMAX",
                    "is_original_language": False,
                    "is_3d": False,
                    "booking_url": "https://example.com/book/5"
                }
            ]
        },
        {
            "title": "The Zone of Interest",
            "original_title": "The Zone of Interest",
            "date": date,
            "image_url": "https://example.com/zone.jpg",
            "description": "The commandant of Auschwitz, Rudolf Höss, and his wife Hedwig, strive to build a dream life for their family.",
            "duration": 105,
            "genres": ["Drama", "History", "War"],
            "rating": 7.4,
            "showtimes": [
                {
                    "time": "18:15",
                    "theater": "Arthouse Pavilion",
                    "room": "Theater 2",
                    "is_original_language": True,
                    "is_3d": False,
                    "booking_url": "https://example.com/book/6"
                },
                {
                    "time": "21:30",
                    "theater": "Film Forum",
                    "room": "Screen B",
                    "is_original_language": True,
                    "is_3d": False,
                    "booking_url": "https://example.com/book/7"
                }
            ]
        }
    ]
    
    return sample_movies


@app.get("/movies/original/{date}")
async def get_original_language_movies(date: str):
    # Get all movies for the date and filter for original language showtimes
    all_movies = await get_movies_by_date(date)
    
    # Filter movies that have at least one original language showtime
    original_movies = []
    for movie in all_movies:
        original_showtimes = [
            showtime for showtime in movie["showtimes"] 
            if showtime["is_original_language"]
        ]
        if original_showtimes:
            # Create a copy of the movie with only original language showtimes
            filtered_movie = movie.copy()
            filtered_movie["showtimes"] = original_showtimes
            original_movies.append(filtered_movie)
    
    return original_movies


# Add new endpoints for scraping
@app.post("/scrape/now")
async def trigger_scraping(background_tasks: BackgroundTasks):
    """
    Trigger an immediate scraping process for today's movies
    """
    scraper_service = ScraperService()
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Run scraping in background
    background_tasks.add_task(scraper_service.scrape_all_cinemas, date_str)

    return {"message": f"Scraping started for {date_str}"}


@app.post("/scrape/dates")
async def scrape_multiple_dates(background_tasks: BackgroundTasks, days: int = 7):
    """
    Trigger scraping process for the next X days
    """
    scraper_service = ScraperService()
    dates = []

    # Schedule scraping for each day
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        dates.append(date_str)
        background_tasks.add_task(scraper_service.scrape_all_cinemas, date_str)

    return {"message": f"Scraping started for dates: {dates}"}


@app.get("/theaters")
async def get_theaters():
    # In a real implementation, this would query the database
    # For now, we'll return some sample data
    theaters = [
        {
            "id": "1",
            "name": "Grand Cinema City",
            "address": "123 Movie Street",
            "city": "Filmtown",
            "website": "https://grandcinemacity.com",
            "phone": "555-123-4567",
            "features": ["IMAX", "4DX", "VIP Seating", "Original Language"]
        },
        {
            "id": "2",
            "name": "Arthouse Pavilion",
            "address": "45 Independent Avenue",
            "city": "Filmtown",
            "website": "https://arthousepavilion.com",
            "phone": "555-987-6543",
            "features": ["Original Language", "Film Festivals", "Director Q&As"]
        },
        {
            "id": "3",
            "name": "Megaplex 20",
            "address": "789 Blockbuster Boulevard",
            "city": "Screenville",
            "website": "https://megaplex20.com",
            "phone": "555-246-8101",
            "features": ["IMAX", "3D", "Dolby Atmos", "SCREENX"]
        },
        {
            "id": "4",
            "name": "Film Forum",
            "address": "321 Classic Road",
            "city": "Cinema City",
            "website": "https://filmforum.com",
            "phone": "555-369-8520",
            "features": ["Original Language", "Classic Films", "Student Discounts"]
        }
    ]
    return theaters


@app.get("/theaters/{theater_id}")
async def get_theater(theater_id: str):
    # In a real implementation, this would query the database
    theaters = {
        "1": {
            "id": "1",
            "name": "Grand Cinema City",
            "address": "123 Movie Street",
            "city": "Filmtown",
            "website": "https://grandcinemacity.com",
            "phone": "555-123-4567",
            "features": ["IMAX", "4DX", "VIP Seating", "Original Language"]
        },
        "2": {
            "id": "2",
            "name": "Arthouse Pavilion",
            "address": "45 Independent Avenue",
            "city": "Filmtown",
            "website": "https://arthousepavilion.com",
            "phone": "555-987-6543",
            "features": ["Original Language", "Film Festivals", "Director Q&As"]
        },
        "3": {
            "id": "3",
            "name": "Megaplex 20",
            "address": "789 Blockbuster Boulevard",
            "city": "Screenville",
            "website": "https://megaplex20.com",
            "phone": "555-246-8101",
            "features": ["IMAX", "3D", "Dolby Atmos", "SCREENX"]
        },
        "4": {
            "id": "4",
            "name": "Film Forum",
            "address": "321 Classic Road",
            "city": "Cinema City",
            "website": "https://filmforum.com",
            "phone": "555-369-8520",
            "features": ["Original Language", "Classic Films", "Student Discounts"]
        }
    }

    theater = theaters.get(theater_id)
    if not theater:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
