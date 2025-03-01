import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import BASE_URL, SELECTORS, MAX_WORKERS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class BlogScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        })
    
    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error obteniendo {url}: {str(e)}")
            return None
    
    def _get_all_pages(self) -> List[str]:
        pages = [BASE_URL]
        current_url = BASE_URL
        
        while True:
            soup = self._get_soup(current_url)
            if not soup:
                break
            
            next_page = soup.select_one(SELECTORS["next_page"])
            if not next_page or not next_page.get("href"):
                break
                
            next_url = urljoin(current_url, next_page["href"])
            if next_url in pages:
                break
                
            pages.append(next_url)
            current_url = next_url
        
        return pages
    
    def get_all_article_links(self) -> List[str]:
        all_links = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self._process_page, page) for page in self._get_all_pages()]
            for future in as_completed(futures):
                all_links.extend(future.result())
        
        return list(set(all_links))
    
    def _process_page(self, page_url: str) -> List[str]:
        soup = self._get_soup(page_url)
        return [
            urljoin(page_url, a["href"])
            for a in soup.select(SELECTORS["article_links"])
            if a.has_attr("href")
        ] if soup else []
    
    def extract_articles(self, urls: List[str]) -> List[Dict]:
        articles = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self._extract_article, url): url for url in urls}
            for future in as_completed(futures):
                if article := future.result():
                    articles.append(article)
        return articles
    
    def _extract_article(self, url: str) -> Optional[Dict]:
        soup = self._get_soup(url)
        if not soup:
            return None
            
        try:
            return {
                "title": soup.select_one(SELECTORS["title"]).text.strip(),
                "content": soup.select_one(SELECTORS["content"]).text.strip(),
                "date": soup.select_one(SELECTORS["date"]).text.strip(),
                "url": url
            }
        except AttributeError as e:
            logger.error(f"Error en {url}: {str(e)}")
            return None