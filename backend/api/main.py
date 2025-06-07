from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta

# Import models and services
from models.supabase import init_database
from models.movie import Movie
from models.repository import MovieRepository, TheaterRepository
from scraper.scraper_service import ScraperService
from datetime import datetime

app = FastAPI(
    title="Movie Observer API",
    description="API for retrieving movie showtimes and language information",
    version="1.0.0"
)

# Setup CORS to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()


@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "Welcome to MovieObserver API"}


@app.get("/movies")
async def get_all_movies():
    """Get all movies from database"""
    try:
        movies = await MovieRepository.get_all_movies()

        # Get showtimes for each movie
        for movie in movies:
            showtimes_data = await MovieRepository.get_movie_with_showtimes(movie["id"])
            if showtimes_data:
                movie["showtimes"] = showtimes_data.get("showtimes", [])
            else:
                movie["showtimes"] = []

        return movies
    except Exception as e:
        print(f"Error fetching movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/movies/{date}")
async def get_movies_by_date(date: str):
    """Get movies for a specific date"""
    try:
        movies = await MovieRepository.get_all_movies(date)

        # Get showtimes for each movie
        for movie in movies:
            showtimes_data = await MovieRepository.get_movie_with_showtimes(movie["id"])
            if showtimes_data:
                movie["showtimes"] = showtimes_data.get("showtimes", [])
            else:
                movie["showtimes"] = []

        return movies
    except Exception as e:
        print(f"Error fetching movies for date {date}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/movies/original/{date}")
async def get_original_language_movies(date: str):
    """Get original language movies for a specific date"""
    try:
        # Get all movies for the given date
        movies = await MovieRepository.get_all_movies(date)

        # Filter movies to include only those with original language showtimes
        result = []
        for movie in movies:
            movie_with_showtimes = await MovieRepository.get_movie_with_showtimes(movie["id"])
            if movie_with_showtimes:
                # Filter showtimes to include only original language
                original_showtimes = [
                    s for s in movie_with_showtimes.get("showtimes", [])
                    if s.get("is_original_language")
                ]

                if original_showtimes:  # Only include movies with original language showtimes
                    movie["showtimes"] = original_showtimes
                    result.append(movie)

        return result
    except Exception as e:
        print(f"Error fetching original language movies for date {date}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/theaters")
async def get_theaters():
    """Get all theaters"""
    try:
        theaters = await TheaterRepository.get_all_theaters()
        return theaters
    except Exception as e:
        print(f"Error fetching theaters: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/theaters/{theater_id}")
async def get_theater(theater_id: int):
    """Get theater by ID"""
    try:
        theater = await TheaterRepository.get_theater(theater_id)

        if not theater:
            raise HTTPException(status_code=404, detail="Theater not found")

        return theater
    except Exception as e:
        print(f"Error fetching theater {theater_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scrape")
async def trigger_scrape(background_tasks: BackgroundTasks, date: Optional[str] = None):
    """Trigger a scrape for a specific date or today"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    scraper_service = ScraperService()

    # Run in background to avoid long response time
    background_tasks.add_task(scraper_service.scrape_all_cinemas, date)

    return {"message": f"Scraping started for date {date}"}


@app.post("/scrape/schedule")
async def schedule_scrape(background_tasks: BackgroundTasks, days: int = 7):
    """Schedule scraping for multiple days ahead"""
    scraper_service = ScraperService()

    # Run in background
    background_tasks.add_task(scraper_service.schedule_daily_scraping, days)

    return {"message": f"Scheduled scraping for {days} days ahead"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
