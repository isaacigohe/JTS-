import requests
from utils.config import SCRAPER_USER_AGENT, SCRAPER_TIMEOUT

class BaseScraper:
    def __init__(self):
        self.headers = {"User-Agent": SCRAPER_USER_AGENT}
        self.timeout = SCRAPER_TIMEOUT

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_job_listing(self, html_content):
        # This method should be overridden by specific scrapers
        raise NotImplementedError("Subclasses must implement parse_job_listing")

    def scrape_jobs(self, keyword=None, location=None):
        # This method should be overridden by specific scrapers
        raise NotImplementedError("Subclasses must implement scrape_jobs")
