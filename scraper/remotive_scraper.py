import requests
from scraper.base_scraper import BaseScraper

class RemotiveScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.api_url = "https://remotive.com/api/remote-jobs"

    def scrape_jobs(self, category="software-dev"):
        print(f"Scraping Remotive ({category})...")
        try:
            params = {"category": category}
            response = requests.get(self.api_url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # FORCE standard UTF-8 text encoding to clear up paragraph symbols
            response.encoding = 'utf-8'
            data = response.json()
            
            job_listings = data.get("jobs", [])
            
            formatted_jobs = []
            for job in job_listings:
                formatted_jobs.append({
                    "source": "Remotive",
                    "job_id": job.get("id"),
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("candidate_required_location", "Remote"),
                    "description": job.get("description"),
                    "url": job.get("url"),
                    "salary": job.get("salary", "Not specified"),
                    "tags": job.get("tags", []),
                    "date_posted": job.get("publication_date")
                })
            return formatted_jobs
        except Exception as e:
            print(f"Error scraping Remotive: {e}")
            return []