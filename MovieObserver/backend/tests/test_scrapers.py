from scraper.cinema_scraper import CinemaScraper
from scraper.spaziocinema_scraper import SpaziocinemaInfoScraper
from scraper.uci_cinemas_scraper import UCICinemasScraper
import logging
import sys
import os
from datetime import datetime
import traceback

from scraper.cinema_scraper import CinemaScraper
from scraper.spaziocinema_scraper import SpaziocinemaInfoScraper
from scraper.uci_cinemas_scraper import UCICinemasScraper

# Now import using relative path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


def test_single_scraper(scraper, date_str=None):
    """Test a single scraper and print results"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"Testing {scraper.__class__.__name__} for date {date_str}")

    try:
        logger.info(f"Getting page content from {scraper.base_url}")
        movies = scraper.get_movies_for_date(date_str)
        logger.info(f"SUCCESS! Found {len(movies)} movies")

        # Print first 2 movies with details
        if movies:
            logger.info("Sample movies:")
            for i, movie in enumerate(movies[:2]):
                logger.info(f"Movie {i+1}: {movie}")
        return movies
    except Exception as e:
        logger.error(f"FAILED: {e}")
        logger.error(traceback.format_exc())
        return []


if __name__ == "__main__":
    # Test Spazio Cinema scraper specifically
    scraper = SpaziocinemaInfoScraper("https://www.spaziocinema.info")

    print("\n" + "="*50)
    logger.info("Testing SpaziocinemaInfoScraper")
    movies = test_single_scraper(scraper)
    print("="*50 + "\n")

    # If you want to test other scrapers:
    scrapers = [
        UCICinemasScraper("https://ucicinemas.it"),
        SpaziocinemaInfoScraper("https://www.spaziocinema.info"),
        CinemaScraper("https://www.example-cinema.com")
    ]

    for scraper in scrapers:
        print("\n" + "="*50)
        movies = test_single_scraper(scraper)
        print("="*50 + "\n")
