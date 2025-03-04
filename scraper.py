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
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Accept-Language": "es-ES,es;q=0.8"
        })
    
    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            
            # Debug: Mostrar primeras líneas del HTML
            if url == BASE_URL:
                logger.debug(f"HTML recibido:\n{response.text[:300]}...")
                
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(f"Error en {url}: {type(e).__name__} - {str(e)}")
            return None
    
    def get_all_article_links(self) -> List[str]:
        all_links = []
        current_url = BASE_URL
        
        while True:
            soup = self._get_soup(current_url)
            if not soup:
                break
            
            # Extraer enlaces de la página actual
            links = soup.select(SELECTORS["article_links"])
            logger.debug(f"Encontrados {len(links)} enlaces en {current_url}")
            
            for link in links:
                if href := link.get('href'):
                    full_url = urljoin(current_url, href)
                    all_links.append(full_url)
            
            # Manejar paginación
            next_page = soup.select_one(SELECTORS["next_page"])
            if not next_page or not next_page.get('href'):
                break
                
            current_url = urljoin(current_url, next_page['href'])
            if current_url in all_links:  # Prevenir loops
                break
        
        return list(set(all_links))  # Eliminar duplicados
    
    def extract_articles(self, urls: List[str]) -> List[Dict]:
        articles = []
        
        for url in urls:
            if article := self._extract_article(url):
                articles.append(article)
                logger.debug(f"Procesado: {article['title'][:30]}...")
        
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
            logger.error(f"Elemento faltante en {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error procesando {url}: {str(e)}")
            return None