import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import logging
from config import BASE_URL, SELECTORS

logger = logging.getLogger(__name__)

class BlogScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        })
        
    def _get_soup(self, url: str) -> BeautifulSoup:
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
        
    def get_article_links(self) -> List[str]:
        soup = self._get_soup(BASE_URL)
        return [urljoin(BASE_URL, a['href']) for a in soup.select(SELECTORS['article_links'])]
    
    def extract_article(self, url: str) -> Dict:
        soup = self._get_soup(url)
        try:
            return {
                "title": soup.select_one(SELECTORS['title']).text.strip(),
                "content": soup.select_one(SELECTORS['content']).text.strip(),
                "date": soup.select_one(SELECTORS['date']).text.strip(),
                "url": url
            }
        except AttributeError as e:
            logger.warning(f"Missing element in {url}: {str(e)}")
            return None