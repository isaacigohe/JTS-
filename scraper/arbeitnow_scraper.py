import requests
from scraper.base_scraper import BaseScraper

class ArbeitnowScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        # Stable, completely public zero-auth JSON endpoint for tech jobs
        self.api_url = "https://www.arbeitnow.com/api/job-board-api"

    def scrape_jobs(self):
        print("⚡ Scraping Arbeitnow Tech Jobs...")
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            response.encoding = 'utf-8'
            data = response.json()
            
            # Arbeitnow returns an array of jobs inside the 'data' key
            job_listings = data.get("data", [])
            print(f"📡 Arbeitnow found {len(job_listings)} tech jobs.")
            
            formatted_jobs = []
            for job in job_listings:
                formatted_jobs.append({
                    "source": "Arbeitnow",
                    "job_id": job.get("slug"), # Unique URL slug used as ID
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("location", "Remote"),
                    "description": job.get("description"), # Raw HTML description handled by main_gui.py
                    "url": job.get("url"), # The direct application link
                    "salary": "Not specified",
                    "tags": job.get("tags", []),
                    "date_posted": job.get("created_at")
                })
            return formatted_jobs
        except Exception as e:
            print(f" Error scraping Arbeitnow: {e}")
            return []