import requests
from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper

class FuzuScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.fuzu.com/job/computers-software-development"

    def scrape_jobs(self):
        print("Scraping Fuzu...")
        html = self.fetch_page(self.base_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        # Fuzu job listing structure
        job_cards = soup.find_all('div', class_='JobCard-module_jobCard__2-p-y')
        
        formatted_jobs = []
        for card in job_cards:
            try:
                title_elem = card.find('h6')
                company_elem = card.find('p', class_='JobCard-module_companyName__3-p-y')
                location_elem = card.find('p', class_='JobCard-module_location__3-p-y')
                
                if title_elem:
                    formatted_jobs.append({
                        "source": "Fuzu",
                        "job_id": "fuzu_" + title_elem.text.strip().replace(" ", "_"),
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip() if company_elem else "Unknown",
                        "location": location_elem.text.strip() if location_elem else "Africa",
                        "description": "View on Fuzu website",
                        "url": "https://www.fuzu.com" + card.find('a')['href'] if card.find('a') else self.base_url,
                        "salary": "Not specified",
                        "tags": ["tech"],
                        "date_posted": "Recent"
                    })
            except Exception as e:
                print(f"Error parsing Fuzu job: {e}")
                
        return formatted_jobs
