import requests
from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper

class DiceScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.dice.com/jobs"

    def scrape_jobs(self, keyword="python"):
        print(f"Scraping Dice for {keyword}...")
        url = f"{self.base_url}?q={keyword}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&language=en"
        html = self.fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        # Dice uses dynamic loading, but some initial data might be in the HTML or we can target specific tags
        # For this simulation, we'll look for common job card patterns
        job_cards = soup.find_all('div', class_='card')
        
        formatted_jobs = []
        for card in job_cards:
            try:
                title_elem = card.find('a', class_='card-title-link')
                company_elem = card.find('a', id='search-result-company-name')
                location_elem = card.find('span', class_='search-result-location')
                
                if title_elem and company_elem:
                    formatted_jobs.append({
                        "source": "Dice",
                        "job_id": title_elem.get('id', 'N/A'),
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else "Remote",
                        "description": "View on Dice website",
                        "url": title_elem['href'],
                        "salary": "Not specified",
                        "tags": [keyword],
                        "date_posted": "Recent"
                    })
            except Exception as e:
                print(f"Error parsing Dice job: {e}")
                
        return formatted_jobs
