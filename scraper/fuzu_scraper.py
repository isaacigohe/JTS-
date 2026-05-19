import requests
from bs4 import BeautifulSoup

class FuzuScraper:
    def __init__(self):
        # Targeting Fuzu's public Kenya job listings feed
        self.url = "https://www.fuzu.com/kenya/job"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def scrape_jobs(self):
        job_list = []
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"[Fuzu] Failed to fetch page. Status: {response.status_code}")
                return job_list

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Fuzu structures posts inside anchor elements containing specific card tracks
            job_cards = soup.find_all('a', href=True)
            
            for card in job_cards:
                # Find titles and company listings within the structural layout cards
                title_tag = card.find('h2') or card.find('h3') or card.find(class_=lambda x: x and 'title' in x.lower())
                
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    
                    # Extract text info safely from parent card bodies
                    card_text = card.get_text("||", strip=True)
                    details = card_text.split("||")
                    
                    # Basic positional extraction based on Fuzu's layout sequence
                    company = "Unknown Company"
                    location = "Nairobi, Kenya"
                    
                    if len(details) > 1:
                        company = details[0] if details[0] != title else details[1]

                    # Resolve relative links into complete structural URLs
                    href = card['href']
                    full_url = href if href.startswith('http') else f"https://www.fuzu.com{href}"
                    
                    job_list.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "source": "Fuzu",
                        "url": full_url,
                        "description": f"Position available at {company}. Double-click or visit Fuzu to view full descriptions and specifications."
                    })
                    
            print(f"[Fuzu] Successfully scraped {len(job_list)} jobs.")
        except Exception as e:
            print(f"Error scraping Fuzu: {e}")
            
        return job_list