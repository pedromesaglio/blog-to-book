import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional
from config import BASE_URL, SELECTORS

logger = logging.getLogger(__name__)

class BlogScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9"
        })
    
    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error en {url}: {type(e).__name__}")
            return None
    
    def _get_paginated_pages(self) -> List[str]:
        pages = []
        current_url = BASE_URL
        
        while True:
            soup = self._get_soup(current_url)
            if not soup:
                break
            
            pages.append(current_url)
            
            # Paginación
            next_btn = soup.select_one(SELECTORS["next_page"])
            if not next_btn or 'href' not in next_btn.attrs:
                break
                
            next_url = urljoin(current_url, next_btn['href'])
            if next_url in pages:
                break
                
            current_url = next_url
        
        return pages
    
    def get_all_article_links(self) -> List[str]:
        all_links = []
        
        for page_url in self._get_paginated_pages():
            soup = self._get_soup(page_url)
            if not soup:
                continue
                
            links = soup.select(SELECTORS["article_links"])
            logger.debug(f"Página {page_url}: {len(links)} enlaces")
            
            for link in links:
                if href := link.get('href'):
                    full_url = urljoin(page_url, href)
                    if full_url not in all_links:
                        all_links.append(full_url)
        
        return all_links
    
    def extract_articles(self, urls: List[str]) -> List[Dict]:
        articles = []
        
        for url in urls:
            if article := self._extract_single_article(url):
                articles.append(article)
        
        return articles
    
    def _extract_single_article(self, url: str) -> Optional[Dict]:
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
            logger.warning(f"Artículo incompleto: {url} - {str(e)}")
            return None