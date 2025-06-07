from typing import List, Dict, Any
from bs4 import BeautifulSoup
import re
import logging
from datetime import datetime
from models.movie import Showtime
from scraper.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class SpaziocinemaInfoScraper(BaseScraper):
    """
    Scraper for Spazio Cinema Milano (https://www.spaziocinema.info/milano)
    """

    def __init__(self, base_url: str = "https://www.spaziocinema.info"):
        super().__init__(base_url)
        self.city = "milano"
        self.theater_name = "Spazio Cinema Milano"

    def get_movies_for_date(self, date: str) -> List[Dict[str, Any]]:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d-%m-%Y")
        url = f"{self.base_url}/{self.city}/programmazione?data={formatted_date}"

        logger.info(f"Scraping movies from {url}")
        html_content = self.get_page_with_selenium(url)
        if not html_content:
            logger.error("Failed to retrieve page content.")
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        movie_sections = soup.select('.movie-list .movie-card')

        movies = []

        for section in movie_sections:
            try:
                title_elem = section.select_one(".movie-title")
                if not title_elem:
                    continue
                title = title_elem.text.strip()

                # Optional: original title from a <span class="original-title">
                original_title_elem = section.select_one(".original-title")
                original_title = original_title_elem.text.strip() if original_title_elem else None

                # Optional description
                description_elem = section.select_one(".movie-synopsis")
                description = description_elem.text.strip() if description_elem else None

                # Optional image
                image_elem = section.select_one("img")
                image_url = f"{self.base_url}{image_elem['src']}" if image_elem and image_elem.has_attr(
                    "src") else None

                # Optional duration
                duration_elem = section.select_one(".movie-duration")
                duration = None
                if duration_elem:
                    match = re.search(r"(\d+)\s*min", duration_elem.text)
                    if match:
                        duration = int(match.group(1))

                # Genres
                genres_elem = section.select_one(".movie-genre")
                genres = [g.strip() for g in re.split(
                    r',|/', genres_elem.text.strip())] if genres_elem else []

                # Showtimes
                showtime_elems = section.select(".movie-times .time")
                showtimes = []
                for time_elem in showtime_elems:
                    time_text = time_elem.text.strip()
                    is_original = bool(
                        re.search(r'v\.?o\.?|sottotit', time_text, re.IGNORECASE))
                    is_3d = '3D' in time_text

                    booking_url = None
                    link = time_elem.find("a")
                    if link and link.has_attr("href"):
                        booking_url = f"{self.base_url}{link['href']}" if link['href'].startswith(
                            "/") else link['href']

                    showtimes.append({
                        "time": time_text,
                        "theater": self.theater_name,
                        "room": "Sala standard",
                        "is_original_language": is_original,
                        "is_3d": is_3d,
                        "booking_url": booking_url,
                    })

                if showtimes:
                    movies.append({
                        "title": title,
                        "original_title": original_title,
                        "date": date,
                        "image_url": image_url,
                        "description": description,
                        "duration": duration,
                        "genres": genres or None,
                        "rating": None,
                        "showtimes": showtimes,
                    })
            except Exception as e:
                logger.error(f"Error parsing movie section: {e}")
                continue

        logger.info(f"Extracted {len(movies)} movies for {date}")
        return movies

    def set_city(self, city: str) -> None:
        self.city = city.lower()

    def get_movie_details(self, movie_url: str) -> Dict[str, Any]:
        logger.info(f"Fetching movie details from {movie_url}")
        html_content = self.get_page_content(movie_url)
        if not html_content:
            return {}

        soup = BeautifulSoup(html_content, 'lxml')
        details = {}

        # Extract director, cast, country, year
        mappings = {
            'director': ['.regia', '.director'],
            'cast': ['.cast'],
            'country': ['.paese', '.country'],
            'year': ['.anno', '.year']
        }

        for key, selectors in mappings.items():
            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.text.strip()
                    if key == 'year':
                        match = re.search(r'\d{4}', text)
                        details[key] = match.group(0) if match else None
                    else:
                        details[key] = text
                    break

        return details
