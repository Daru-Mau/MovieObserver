from typing import List, Dict, Any
from bs4 import BeautifulSoup
from models.movie import Showtime
from scraper.base_scraper import BaseScraper
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class CinessaScraper(BaseScraper):
    """
    Scraper implementation for Cinessa Cinemas (example)
    """

    def __init__(self, base_url: str = "https://cinessa.com"):
        super().__init__(base_url)

    def get_movies_for_date(self, date: str) -> List[Dict[str, Any]]:
        """
        Get all movies for a specific date from Cinessa Cinemas

        Args:
            date (str): Date in format YYYY-MM-DD

        Returns:
            List[Dict[str, Any]]: List of movie data
        """
        # Convert date string to required format (if needed)
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%Y/%m/%d")  # Adjust format as needed
        
        # Construct the URL for the specific date
        url = f"{self.base_url}/movies/showtimes/{formatted_date}"
        logger.info(f"Scraping movies from {url}")

        # Get the page content using standard requests (if the site doesn't require JS)
        html_content = self.get_page_content(url)

        if not html_content:
            logger.error(f"Failed to get content from {url}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'lxml')

        # Find all movie containers (adjust selector based on actual website structure)
        movie_containers = soup.select('.movie-item')  # Replace with actual selector

        movies = []

        for container in movie_containers:
            try:
                # Extract movie details (adjust selectors based on actual website structure)
                title = container.select_one('.movie-name').text.strip()
                original_title_elem = container.select_one('.original-name')
                original_title = original_title_elem.text.strip() if original_title_elem else title
                
                # Determine if movie is in original language
                is_original_language = any(['VOSE' in tag.text or 'V.O.' in tag.text 
                                          for tag in container.select('.language-indicator')])
                
                # Extract showtime information
                showtime_elements = container.select('.showtime-slot')
                showtimes = []
                
                for element in showtime_elements:
                    time_str = element.select_one('.time').text.strip()
                    # Check if this showtime is in original language
                    is_vo = any(['VOSE' in tag.text or 'V.O.' in tag.text 
                               for tag in element.select('.format')])
                    
                    room_element = element.select_one('.room')
                    theater_screen = room_element.text.strip() if room_element else "Standard"
                    
                    showtime = Showtime(
                        time=time_str,
                        is_original_language=is_vo,
                        theater_screen=theater_screen,
                        booking_url=f"{self.base_url}{element.select_one('a').get('href')}" 
                                   if element.select_one('a') else None
                    )
                    showtimes.append(showtime.dict())
                
                # Create movie object
                movie = {
                    "title": title,
                    "original_title": original_title,
                    "poster_url": container.select_one('img.poster').get('src') if container.select_one('img.poster') else None,
                    "synopsis": container.select_one('.description').text.strip() if container.select_one('.description') else "",
                    "duration": self._extract_duration(container.select_one('.runtime').text) if container.select_one('.runtime') else None,
                    "is_original_language": is_original_language,
                    "genres": [tag.text.strip() for tag in container.select('.genre-tag')],
                    "showtimes": showtimes,
                    "theater": "Cinessa Cinemas",
                    "url": f"{self.base_url}{container.select_one('a.details').get('href')}" 
                          if container.select_one('a.details') else None
                }
                
                movies.append(movie)
                
            except Exception as e:
                logger.error(f"Error parsing movie: {e}")
                continue
                
        logger.info(f"Scraped {len(movies)} movies from Cinessa Cinemas")
        return movies
    
    def _extract_duration(self, duration_text: str) -> int:
        """Extract movie duration in minutes from text"""
        if not duration_text:
            return None
            
        match = re.search(r'(\d+)\s*min', duration_text)
        if match:
            return int(match.group(1))
        return None
