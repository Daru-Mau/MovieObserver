import logging
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Import database repository
from models.repository import MovieRepository

# Import scrapers
from scraper.cinema_scraper import CinemaScraper
from scraper.uci_cinemas_scraper import UCICinemasScraper
from scraper.spaziocinema_scraper import SpaziocinemaInfoScraper

logger = logging.getLogger(__name__)


class ScraperService:
    """
    Service to manage scraping operations from different cinema websites
    """

    def __init__(self):
        # No need to store DB instance, we'll get client when needed
        self.scrapers = [
            # Real cinema website scrapers
            UCICinemasScraper("https://ucicinemas.it"),
            SpaziocinemaInfoScraper("https://www.spaziocinema.info"),

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
                logger.info(f"Starting scraping with {scraper.__class__.__name__} for date {date_str}")
                movies = scraper.get_movies_for_date(date_str)
                
                if movies:
                    logger.info(f"Successfully scraped {len(movies)} movies from {scraper.__class__.__name__}")
                    all_movies.extend(movies)
                else:
                    logger.warning(f"No movies found from {scraper.__class__.__name__} for date {date_str}")
            except Exception as e:
                logger.error(
                    f"Error scraping with {scraper.__class__.__name__}: {str(e)}", exc_info=True)

        if all_movies:
            # Store movies in database using repository
            for movie in all_movies:
                try:
                    # Make sure date is consistent
                    movie["date"] = date_str
                    # Use repository to insert or update movie
                    await MovieRepository.insert_or_update_movie(movie)
                except Exception as e:
                    logger.error(f"Error storing movie {movie['title']}: {e}")

            logger.info(f"Updated {len(all_movies)} movies in database")

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