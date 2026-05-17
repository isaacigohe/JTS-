import requests
from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper

class NoDeskScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://nodesk.co/remote-jobs/"

    def scrape_jobs(self):
        print("Scraping NoDesk...")
        html = self.fetch_page(self.base_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        job_cards = soup.find_all('tr', class_='job') # Based on common structure, might need adjustment
        
        formatted_jobs = []
        # Note: NoDesk structure might be complex, this is a simplified version
        # In a real scenario, we'd inspect the exact classes
        for card in job_cards:
            try:
                title_elem = card.find('a', class_='job-title')
                company_elem = card.find('a', class_='job-company')
                
                if title_elem and company_elem:
                    formatted_jobs.append({
                        "source": "NoDesk",
                        "job_id": card.get('id', 'N/A'),
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": "Remote",
                        "description": "View on website",
                        "url": "https://nodesk.co" + title_elem['href'],
                        "salary": "Not specified",
                        "tags": [],
                        "date_posted": "N/A"
                    })
            except Exception as e:
                print(f"Error parsing NoDesk job: {e}")
                
        return formatted_jobs
