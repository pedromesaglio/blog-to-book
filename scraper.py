import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Optional, Union
import time
import random
from config import BASE_URL, SELECTORS, MAX_PAGES

logger = logging.getLogger(__name__)

class BlogScraper:
    def __init__(self, delay_range: tuple = (1, 3), max_retries: int = 3):
        self.session = requests.Session()
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.visited_urls = set()
        self._configure_session()
        self._validate_base_url()

    def _configure_session(self):
        """Configura la sesión HTTP con retries y headers"""
        retries = requests.adapters.Retry(
            total=self.max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9",
            "Referer": BASE_URL
        })

    def _validate_base_url(self):
        """Valida que la URL base sea correcta"""
        parsed = urlparse(BASE_URL)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"URL base inválida: {BASE_URL}")

    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Obtiene el contenido parseado de una URL"""
        try:
            self._respect_delay()
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            logger.error(f"Error obteniendo {url}: {type(e).__name__}")
            return None

    def _respect_delay(self):
        """Respeta el tiempo de espera entre requests"""
        if self.delay_range:
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)

    def get_all_article_links(self) -> List[str]:
        """Obtiene todos los enlaces a artículos"""
        all_links = set()
        current_url = BASE_URL
        pages_processed = 0

        while pages_processed < MAX_PAGES:
            soup = self._get_soup(current_url)
            if not soup:
                break

            # Extraer enlaces de artículos
            new_links = self._extract_links_from_page(soup, current_url)
            all_links.update(new_links)
            logger.info(f"Página {pages_processed + 1}: {len(new_links)} enlaces")

            # Obtener siguiente página
            current_url = self._get_next_page(soup, current_url)
            if not current_url or current_url in self.visited_urls:
                break

            pages_processed += 1
            self.visited_urls.add(current_url)

        return list(all_links)

    def _extract_links_from_page(self, soup: BeautifulSoup, base_url: str) -> set:
        """Extrae enlaces válidos de una página"""
        links = set()
        for selector in SELECTORS["article_links"]:
            for link in soup.select(selector):
                if href := link.get('href'):
                    full_url = urljoin(base_url, href)
                    if self._is_valid_article_url(full_url):
                        links.add(full_url)
        return links

    def _get_next_page(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        """Obtiene la URL de la siguiente página"""
        for selector in SELECTORS["next_page"]:
            next_btn = soup.select_one(selector)
            if next_btn and next_btn.get('href'):
                next_url = urljoin(current_url, next_btn['href'])
                parsed_next = urlparse(next_url)
                if parsed_next.netloc == urlparse(BASE_URL).netloc:
                    return next_url
        return None

    def _is_valid_article_url(self, url: str) -> bool:
        """Valida si una URL corresponde a un artículo válido"""
        parsed = urlparse(url)
        return (
            parsed.netloc == urlparse(BASE_URL).netloc and
            parsed.path.strip('/') != '' and
            url not in self.visited_urls
        )

    def extract_articles(self, urls: List[str]) -> List[Dict]:
        """Extrae el contenido de los artículos"""
        articles = []
        for url in urls:
            if article := self._extract_single_article(url):
                articles.append(article)
        return articles

    def _extract_single_article(self, url: str) -> Optional[Dict]:
        """Extrae el contenido de un artículo individual"""
        soup = self._get_soup(url)
        if not soup:
            return None

        try:
            article_data = {
                "title": self._safe_extract(soup, "title"),
                "content": self._safe_extract(soup, "content"),
                "date": self._safe_extract(soup, "date", is_date=True),
                "url": url
            }

            if not article_data["title"] and not article_data["content"]:
                logger.warning(f"Artículo vacío: {url}")
                return None

            return article_data
        except Exception as e:
            logger.error(f"Error procesando {url}: {str(e)}")
            return None

    def _safe_extract(self, soup: BeautifulSoup, field: str, is_date: bool = False) -> str:
        """Extrae contenido de manera segura usando selectores alternativos"""
        selectors = SELECTORS.get(field, [])
        if not isinstance(selectors, list):
            selectors = [selectors]

        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    if is_date and 'datetime' in selector:
                        return element.get('datetime', '').strip()
                    return element.get_text(separator=' ', strip=True)
            except Exception as e:
                logger.debug(f"Selector fallido {selector}: {str(e)}")

        return ""