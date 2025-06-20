import logging
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class for all movie scrapers
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    @abstractmethod
    def get_movies_for_date(self, date: str) -> List[Dict[str, Any]]:
        """
        Get all movies for a specific date

        Args:
            date (str): Date in format YYYY-MM-DD

        Returns:
            List[Dict[str, Any]]: List of movie data
        """
        pass

    def get_page_content(self, url: str) -> Optional[str]:
        """
        Get the HTML content of a page

        Args:
            url (str): URL to fetch

        Returns:
            Optional[str]: HTML content or None if request failed
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
            
    def get_page_with_selenium(self, url: str) -> Optional[str]:
        """
        Get the HTML content of a page using Selenium (for JavaScript-rendered content)

        Args:
            url (str): URL to fetch

        Returns:
            Optional[str]: HTML content or None if request failed
        """
        try:
            # Check which WebDriver to use based on env settings
            firefox_driver_path = os.getenv('FIREFOX_DRIVER_PATH')
            chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
            
            if firefox_driver_path is not None:
                # Use Firefox WebDriver
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--headless")
                
                if firefox_driver_path.lower() == 'none':
                    service = FirefoxService(GeckoDriverManager().install())
                else:
                    service = FirefoxService(firefox_driver_path)
                
                logger.info("Using Firefox WebDriver")
                driver = webdriver.Firefox(service=service, options=firefox_options)
            else:
                # Use Chrome WebDriver as fallback
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                
                if chrome_driver_path:
                    service = ChromeService(chrome_driver_path)
                else:
                    service = ChromeService(ChromeDriverManager().install())
                
                logger.info("Using Chrome WebDriver")
                driver = webdriver.Chrome(service=service, options=chrome_options)

            logger.info(f"Fetching page with Selenium: {url}")
            driver.get(url)
            # Wait for dynamic content to load
            driver.implicitly_wait(10)

            page_source = driver.page_source
            driver.quit()

            return page_source
        except Exception as e:
            logger.error(f"Error fetching {url} with Selenium: {e}")
            return None