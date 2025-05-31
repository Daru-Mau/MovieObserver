from typing import List, Dict, Any
from bs4 import BeautifulSoup
from models.movie import Showtime
from scraper.base_scraper import BaseScraper
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class YelmoScraper(BaseScraper):
    """
    Scraper implementation for Yelmo Cinemas (Spain)
    """

    def __init__(self, base_url: str = "https://yelmocines.es"):
        super().__init__(base_url)

    def get_movies_for_date(self, date: str) -> List[Dict[str, Any]]:
        """
        Get all movies for a specific date from Yelmo Cinemas

        Args:
            date (str): Date in format YYYY-MM-DD

        Returns:
            List[Dict[str, Any]]: List of movie data
        """
        # Convert date string to required format (if needed)
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d-%m-%Y")  # Adjust format as needed
        
        # Construct the URL for the specific date
        url = f"{self.base_url}/cartelera/#{formatted_date}"
        logger.info(f"Scraping movies from {url}")

        # Get the page content using Selenium for JS-rendered content
        html_content = self.get_page_with_selenium(url)

        if not html_content:
            logger.error(f"Failed to get content from {url}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'lxml')

        # Find all movie containers (adjust selector based on actual website structure)
        movie_containers = soup.select('.movie-container')  # Replace with actual selector

        movies = []

        for container in movie_containers:
            try:
                # Extract movie details (adjust selectors based on actual website structure)
                title = container.select_one('.movie-title').text.strip()
                original_title_elem = container.select_one('.original-title')
                original_title = original_title_elem.text.strip() if original_title_elem else title
                
                # Determine if movie is in original language
                is_original_language = any('V.O.' in tag.text for tag in container.select('.language-tag'))
                
                # Extract showtime information
                showtime_elements = container.select('.showtime')
                showtimes = []
                
                for element in showtime_elements:
                    time_str = element.text.strip()
                    # Check if this showtime is in original language
                    is_vo = 'V.O.' in element.parent.text
                    
                    showtime = Showtime(
                        time=time_str,
                        is_original_language=is_vo,
                        theater_screen="Standard",  # Default value, update if available
                        booking_url=f"{self.base_url}{element.get('href')}" if element.get('href') else None
                    )
                    showtimes.append(showtime.dict())
                
                # Create movie object
                movie = {
                    "title": title,
                    "original_title": original_title,
                    "poster_url": container.select_one('img.poster').get('src') if container.select_one('img.poster') else None,
                    "synopsis": container.select_one('.synopsis').text.strip() if container.select_one('.synopsis') else "",
                    "duration": self._extract_duration(container.select_one('.duration').text) if container.select_one('.duration') else None,
                    "is_original_language": is_original_language,
                    "genres": [tag.text.strip() for tag in container.select('.genre')],
                    "showtimes": showtimes,
                    "theater": "Yelmo Cinemas",
                    "url": f"{self.base_url}{container.select_one('a').get('href')}" if container.select_one('a') else None
                }
                
                movies.append(movie)
                
            except Exception as e:
                logger.error(f"Error parsing movie: {e}")
                continue
                
        logger.info(f"Scraped {len(movies)} movies from Yelmo Cinemas")
        return movies
    
    def _extract_duration(self, duration_text: str) -> int:
        """Extract movie duration in minutes from text"""
        if not duration_text:
            return None
            
        match = re.search(r'(\d+)\s*min', duration_text)
        if match:
            return int(match.group(1))
        return None
