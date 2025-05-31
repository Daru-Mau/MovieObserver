import logging
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Import database
from models.database import get_database

# Import scrapers
from scraper.cinema_scraper import CinemaScraper
from scraper.yelmo_scraper import YelmoScraper
from scraper.cinessa_scraper import CinessaScraper
from scraper.uci_cinemas_scraper import UCICinemasScraper

logger = logging.getLogger(__name__)


class ScraperService:
    """
    Service to manage scraping operations from different cinema websites
    """

    def __init__(self):
        self.db = get_database()
        self.scrapers = [
            # Real cinema website scrapers
            YelmoScraper("https://www.yelmocines.es"),
            CinessaScraper("https://www.cinessa.com"),
            UCICinemasScraper("https://ucicinemas.it"),
            
            # Example scrapers (for testing)
            CinemaScraper("https://www.example-cinema.com"),
            
            # Add more cinema websites as needed
            # Create a new scraper class for each cinema chain with unique HTML structure
        ]

    async def scrape_all_cinemas(self, date_str: str = None) -> None:
        """
        Scrape all cinemas for a specific date

        Args:
            date_str (str, optional): Date in format YYYY-MM-DD. 
                                      If None, today's date is used.
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")

        logger.info(f"Starting scraping for date {date_str}")

        all_movies = []

        for scraper in self.scrapers:
            try:
                movies = scraper.get_movies_for_date(date_str)
                all_movies.extend(movies)
                logger.info(
                    f"Scraped {len(movies)} movies from {scraper.__class__.__name__}")
            except Exception as e:
                logger.error(
                    f"Error scraping with {scraper.__class__.__name__}: {e}")

        if all_movies:
            # Store movies in database
            # Create a bulk operation
            ops = []
            for movie in all_movies:
                # Use upsert to update if exists or insert if not
                ops.append(
                    {
                        "update_one": {
                            "filter": {"title": movie["title"], "date": date_str},
                            "update": {"$set": {**movie, "updated_at": datetime.utcnow()}},
                            "upsert": True
                        }
                    }
                )

            if ops:
                await self.db["movies"].bulk_write(ops)
                logger.info(f"Updated {len(ops)} movies in database")

    async def schedule_daily_scraping(self, days_ahead: int = 7) -> None:
        """
        Schedule scraping for the next N days

        Args:
            days_ahead (int): Number of days to scrape ahead
        """
        today = datetime.now()

        for i in range(days_ahead):
            date = today + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")

            logger.info(f"Scheduling scrape for {date_str}")
            await self.scrape_all_cinemas(date_str)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run the scraper service
    scraper_service = ScraperService()
    asyncio.run(scraper_service.schedule_daily_scraping())
