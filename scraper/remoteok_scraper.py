import requests
import json
from scraper.base_scraper import BaseScraper

class RemoteOKScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.api_url = "https://remoteok.com/api"

    def scrape_jobs(self):
        print("Scraping RemoteOK...")
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # FORCE standard UTF-8 text encoding to fix the weird 'â' characters
            response.encoding = 'utf-8'
            data = response.json()
            
            # RemoteOK API returns a list where the first element is legal info
            job_listings = data[1:]
            
            formatted_jobs = []
            for job in job_listings:
                formatted_jobs.append({
                    "source": "RemoteOK",
                    "job_id": job.get("id"),
                    "title": job.get("position"),
                    "company": job.get("company"),
                    "location": job.get("location", "Remote"),
                    "description": job.get("description"),
                    "url": job.get("url"),
                    "salary": f"{job.get('salary_min', 0)} - {job.get('salary_max', 0)}",
                    "tags": job.get("tags", []),
                    "date_posted": job.get("date")
                })
            return formatted_jobs
        except Exception as e:
            print(f"Error scraping RemoteOK: {e}")
            return []