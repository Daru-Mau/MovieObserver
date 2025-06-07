from typing import List, Dict, Any
from bs4 import BeautifulSoup
from models.movie import Showtime
from scraper.base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class CinemaScraper(BaseScraper):
    """
    Example scraper implementation for a fictional cinema website.
    This is just a template to demonstrate how to implement a specific scraper.
    """

    def __init__(self, base_url: str = "https://example-cinema.com"):
        super().__init__(base_url)

    def get_movies_for_date(self, date: str) -> List[Dict[str, Any]]:
        """
        Get all movies for a specific date

        Args:
            date (str): Date in format YYYY-MM-DD

        Returns:
            List[Dict[str, Any]]: List of movie data
        """
        url = f"{self.base_url}/showtimes/{date}"
        logger.info(f"Scraping movies from {url}")

        # Get the page content using Selenium (for JavaScript-rendered content)
        html_content = self.get_page_with_selenium(url)

        if not html_content:
            logger.error(f"Failed to get content from {url}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'lxml')

        # Find all movie containers
        movie_containers = soup.select('.movie-container')

        movies = []

        for container in movie_containers:
            try:
                # Extract movie details
                title = container.select_one('.movie-title').text.strip()
                original_title_elem = container.select_one(
                    '.movie-original-title')
                original_title = original_title_elem.text.strip() if original_title_elem else None

                # Extract image URL
                image_elem = container.select_one('.movie-poster img')
                image_url = image_elem['src'] if image_elem else None

                # Extract description
                description_elem = container.select_one('.movie-description')
                description = description_elem.text.strip() if description_elem else None

                # Extract duration
                duration_elem = container.select_one('.movie-duration')
                duration = int(duration_elem.text.strip().split(' ')[
                               0]) if duration_elem else None

                # Extract genres
                genres_elems = container.select('.movie-genre')
                genres = [genre.text.strip()
                          for genre in genres_elems] if genres_elems else None

                # Extract rating
                rating_elem = container.select_one('.movie-rating')
                rating = float(rating_elem.text.strip()
                               ) if rating_elem else None

                # Extract showtimes
                showtime_containers = container.select('.movie-showtime')
                showtimes = []

                for showtime_container in showtime_containers:
                    theater = showtime_container.select_one(
                        '.theater-name').text.strip()
                    room = showtime_container.select_one(
                        '.room-number').text.strip()
                    time = showtime_container.select_one(
                        '.showtime-time').text.strip()

                    # Check if it's original language
                    is_original_language = 'original-language' in showtime_container.get('class', [
                    ])

                    # Check if it's 3D
                    is_3d = '3d' in showtime_container.get('class', [])

                    # Get booking URL if available
                    booking_elem = showtime_container.select_one(
                        'a.booking-link')
                    booking_url = booking_elem['href'] if booking_elem else None

                    showtime = {
                        "time": time,
                        "theater": theater,
                        "room": room,
                        "is_original_language": is_original_language,
                        "is_3d": is_3d,
                        "booking_url": booking_url
                    }

                    showtimes.append(showtime)

                # Create movie object
                movie = {
                    "title": title,
                    "original_title": original_title,
                    "date": date,
                    "image_url": image_url,
                    "description": description,
                    "duration": duration,
                    "genres": genres,
                    "rating": rating,
                    "showtimes": showtimes
                }

                movies.append(movie)

            except Exception as e:
                logger.error(f"Error parsing movie: {e}")
                continue

        logger.info(f"Scraped {len(movies)} movies from {url}")
        return movies
