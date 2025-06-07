from typing import List, Dict, Any
from bs4 import BeautifulSoup
from models.movie import Showtime
from scraper.base_scraper import BaseScraper
import logging
import re
from datetime import datetime, timedelta
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class UCICinemasScraper(BaseScraper):
    """
    Scraper implementation for UCI Cinemas (Italy)
    https://ucicinemas.it/
    """

    def __init__(self, base_url: str = "https://ucicinemas.it"):
        super().__init__(base_url)
        self.cinema_list_url = f"{self.base_url}/cinema"
        self.films_list_url = f"{self.base_url}/film"

    def get_movies_for_date(self, date: str) -> List[Dict[str, Any]]:
        """
        Get all movies for a specific date from UCI Cinemas

        Args:
            date (str): Date in format YYYY-MM-DD

        Returns:
            List[Dict[str, Any]]: List of movie data
        """
        # First, get the list of cinemas
        cinemas = self._get_all_cinemas()
        logger.info(f"Found {len(cinemas)} UCI cinema locations")

        # Convert date string to required format for UCI Cinemas
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        # List to store all movie data
        all_movies = []

        # For each cinema, get its showtimes
        for cinema in cinemas[:3]:  # Limit to 3 cinemas to avoid too many requests
            cinema_id = cinema["id"]
            cinema_name = cinema["name"]
            cinema_url = cinema["url"]

            logger.info(f"Scraping movies from {cinema_name} for date {date}")

            # Get showtimes for this cinema on the specified date
            movies = self._get_cinema_showtimes(
                cinema_url, cinema_name, date_obj)

            # Add all movies from this cinema to our list
            all_movies.extend(movies)

            # Sleep to avoid overloading the server
            time.sleep(1)

        # Deduplicate movies by title and add theater information
        unique_movies = self._deduplicate_movies(all_movies)

        logger.info(
            f"Scraped {len(unique_movies)} unique movies from UCI Cinemas")
        return unique_movies

    def _get_all_cinemas(self) -> List[Dict[str, str]]:
        """
        Get all UCI cinema locations

        Returns:
            List[Dict[str, str]]: List of cinema data with id, name and URL
        """
        # Get the cinema list page
        html_content = self.get_page_with_selenium(self.cinema_list_url)

        if not html_content:
            logger.error(f"Failed to get content from {self.cinema_list_url}")
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        cinemas = []

        # Find all cinema links
        cinema_links = soup.select('a[href^="/cinema/uci-cinemas"]')

        for link in cinema_links:
            cinema_url = f"{self.base_url}{link['href']}"
            cinema_name = link.text.strip()

            # Extract the ID from the URL
            cinema_id = link['href'].split('/')[-1]

            cinemas.append({
                "id": cinema_id,
                "name": cinema_name,
                "url": cinema_url
            })

        return cinemas

    def _get_cinema_showtimes(self, cinema_url: str, cinema_name: str, date_obj: datetime) -> List[Dict[str, Any]]:
        """
        Get all movie showtimes for a specific cinema and date

        Args:
            cinema_url (str): URL of the cinema page
            cinema_name (str): Name of the cinema
            date_obj (datetime): Date object

        Returns:
            List[Dict[str, Any]]: List of movie data with showtimes
        """
        movies = []

        # Use Selenium to load the cinema page with JavaScript
        driver = self._get_selenium_driver()
        try:
            driver.get(cinema_url)

            # Wait for the movies to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".movie-container"))
            )

            # Check if there's a calendar selector and select the correct date
            try:
                # First find the calendar element
                calendar = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".calendar-container"))
                )

                # Format the date for the selector (it may use format like "dd MMM" or similar)
                formatted_date = date_obj.strftime("%d/%m")

                # Try to find and click the date
                date_buttons = driver.find_elements(
                    By.CSS_SELECTOR, ".calendar-day")
                for button in date_buttons:
                    if formatted_date in button.text or date_obj.day == int(button.text.strip()):
                        button.click()
                        time.sleep(2)  # Wait for content to refresh
                        break
            except (TimeoutException, NoSuchElementException):
                logger.warning(
                    f"Could not find calendar selector on {cinema_url}")

            # Get the page HTML after any date selection
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'lxml')

            # Find all movie containers
            movie_containers = soup.select('.movie-container')

            for container in movie_containers:
                try:
                    # Extract movie details
                    title_element = container.select_one('.movie-title, h3')
                    title = title_element.text.strip() if title_element else "Unknown Title"

                    # Extract movie description if available
                    description_elem = container.select_one(
                        '.movie-description, p')
                    description = description_elem.text.strip() if description_elem else ""

                    # Extract movie poster if available
                    poster_elem = container.select_one('img')
                    poster_url = poster_elem['src'] if poster_elem and 'src' in poster_elem.attrs else None

                    # Check for original language screenings
                    # Look for "V.O." or "VOSE" (Versión Original Subtitulada en Español) indicators
                    is_original_language = any(tag for tag in container.select('.language-tag, .format')
                                               if tag and ('V.O.' in tag.text or 'VOSE' in tag.text or 'OV' in tag.text))

                    # Extract showtimes
                    showtime_elements = container.select(
                        '.showtimes a, .showtime')
                    showtimes = []

                    for element in showtime_elements:
                        time_text = element.text.strip()
                        if not time_text or time_text.lower() in ['acquista', 'prenota']:
                            continue

                        # Check if this showtime is in original language
                        is_vo = is_original_language or any(tag for tag in element.parent.select('.language-tag, .format')
                                                            if tag and ('V.O.' in tag.text or 'VOSE' in tag.text or 'OV' in tag.text))

                        # Extract booking link if available
                        booking_url = None
                        if element.name == 'a' and 'href' in element.attrs:
                            booking_url = element['href']
                            if not booking_url.startswith('http'):
                                booking_url = f"{self.base_url}{booking_url}"

                        # Extract any format information (3D, IMAX, etc.)
                        format_elem = element.select_one('.format')
                        theater_screen = format_elem.text.strip() if format_elem else "Standard"

                        showtime = Showtime(
                            time=time_text,
                            is_original_language=is_vo,
                            theater_screen=theater_screen,
                            booking_url=booking_url
                        )
                        showtimes.append(showtime.dict())

                    # Skip movies with no showtimes
                    if not showtimes:
                        continue

                    # Extract movie URL if available
                    movie_url_elem = container.select_one('a[href^="/film/"]')
                    movie_url = None
                    if movie_url_elem and 'href' in movie_url_elem.attrs:
                        movie_url = f"{self.base_url}{movie_url_elem['href']}"

                    # Create movie entry
                    movie = {
                        "title": title,
                        "original_title": title,  # Assume same as title, may be updated later
                        "poster_url": poster_url,
                        "synopsis": description,
                        "duration": None,  # Not always available
                        "is_original_language": is_original_language,
                        "genres": [],  # Not easily available on cinema page
                        "showtimes": showtimes,
                        "theater": cinema_name,
                        "theater_id": cinema_url.split('/')[-1],
                        "url": movie_url,
                        "date": date_obj.strftime("%Y-%m-%d")
                    }

                    movies.append(movie)

                except Exception as e:
                    logger.error(f"Error parsing movie in {cinema_name}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error scraping {cinema_url}: {e}")
        finally:
            driver.quit()

        return movies

    def _deduplicate_movies(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate movies by title and combine showtimes

        Args:
            movies (List[Dict[str, Any]]): List of movie data

        Returns:
            List[Dict[str, Any]]: Deduplicated list of movie data
        """
        unique_movies = {}

        for movie in movies:
            title = movie["title"]

            if title not in unique_movies:
                unique_movies[title] = movie
            else:
                # Add this theater's showtimes to the existing movie entry
                existing_movie = unique_movies[title]

                # Add theater to list of theaters showing this movie
                theater_info = {
                    "name": movie["theater"],
                    "id": movie["theater_id"]
                }

                if "theaters" not in existing_movie:
                    existing_movie["theaters"] = [
                        {"name": existing_movie["theater"], "id": existing_movie["theater_id"]}]

                existing_movie["theaters"].append(theater_info)

                # Add showtimes
                existing_movie["showtimes"].extend(movie["showtimes"])

                # Update original language flag if any theater shows it in original language
                if movie["is_original_language"]:
                    existing_movie["is_original_language"] = True

        return list(unique_movies.values())

    def _enrich_movie_details(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get additional movie details from the movie page

        Args:
            movie (Dict[str, Any]): Movie data

        Returns:
            Dict[str, Any]: Enriched movie data
        """
        if not movie["url"]:
            return movie

        try:
            html_content = self.get_page_content(movie["url"])

            if not html_content:
                return movie

            soup = BeautifulSoup(html_content, 'lxml')

            # Try to extract original title if different from title
            original_title_elem = soup.select_one('.original-title')
            if original_title_elem:
                movie["original_title"] = original_title_elem.text.strip()

            # Try to extract duration
            duration_elem = soup.select_one('.duration')
            if duration_elem:
                duration_text = duration_elem.text.strip()
                match = re.search(r'(\d+)', duration_text)
                if match:
                    movie["duration"] = int(match.group(1))

            # Try to extract genres
            genre_elems = soup.select('.genre')
            if genre_elems:
                movie["genres"] = [elem.text.strip() for elem in genre_elems]

        except Exception as e:
            logger.error(
                f"Error enriching movie details for {movie['title']}: {e}")

        return movie
