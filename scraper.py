"""
Módulo para extraer contenido del blog.
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import logging
from config import BASE_URL, HEADERS, SELECTORS

logger = logging.getLogger(__name__)

class BlogScraper:
    """Extrae artículos de un blog."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def _get_soup(self, url: str) -> BeautifulSoup:
        """Retorna el objeto BeautifulSoup de una URL."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error al obtener {url}: {e}")
            raise
    
    def get_article_links(self) -> List[str]:
        """Obtiene URLs de todos los artículos."""
        soup = self._get_soup(BASE_URL)
        links = []
        for link in soup.select(SELECTORS["article_links"]):
            href = link.get("href")
            full_url = urljoin(BASE_URL, href)
            links.append(full_url)
        return links
    
    def extract_article(self, url: str) -> Dict:
        """Extrae contenido de un artículo individual."""
        soup = self._get_soup(url)
        try:
            title = soup.select_one(SELECTORS["title"]).text.strip()
            content = soup.select_one(SELECTORS["content"]).text.strip()
            date = soup.select_one(SELECTORS["date"]).text.strip()
        except AttributeError as e:
            logger.warning(f"Elemento no encontrado en {url}: {e}")
            return None
        
        return {
            "title": title,
            "content": content,
            "date": date,
            "url": url
        }