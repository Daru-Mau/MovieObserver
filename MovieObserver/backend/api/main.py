from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime, timedelta

# Import database connection
from models.database import get_database

# Import movie model
from models.movie import Movie

# Import scraper service
from scraper.scraper_service import ScraperService

app = FastAPI(title="Movie Observer API",
              description="API for retrieving movie showtimes and language information",
              version="1.0.0")

# Setup CORS to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to MovieObserver API"}


@app.get("/movies", response_model=List[Movie])
async def get_all_movies():
    db = get_database()
    movies = await db["movies"].find().to_list(1000)
    return movies


@app.get("/movies/{date}")
async def get_movies_by_date(date: str):
    db = get_database()
    movies = await db["movies"].find({"date": date}).to_list(1000)
    if not movies:
        raise HTTPException(
            status_code=404, detail="No movies found for this date")
    return movies


@app.get("/movies/original/{date}")
async def get_original_language_movies(date: str):
    db = get_database()


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
    movies = await db["movies"].find({
        "date": date,
        "original_language": True
    }).to_list(1000)
    if not movies:
        raise HTTPException(
            status_code=404, detail="No original language movies found for this date")
    return movies


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
