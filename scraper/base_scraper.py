import requests
from utils.config import SCRAPER_USER_AGENT, SCRAPER_TIMEOUT

class BaseScraper:
    def __init__(self):
        # FIX: Provide a fallback real-world browser string if config.py has an empty/bot agent
        user_agent = SCRAPER_USER_AGENT if SCRAPER_USER_AGENT else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json, text/html, application/xhtml+xml, */*",
            "Accept-Language": "en-US,en;q=0.9"
        }
        self.timeout = SCRAPER_TIMEOUT if SCRAPER_TIMEOUT else 10

    def fetch_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_job_listing(self, html_content):
        raise NotImplementedError("Subclasses must implement parse_job_listing")

    def scrape_jobs(self, keyword=None, location=None):
        raise NotImplementedError("Subclasses must implement scrape_jobs")