import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import time
import random
from typing import List, Dict, Optional
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from config import BASE_URL, SELECTORS, MAX_PAGES, REQUEST_DELAY, MAX_RETRIES

logger = logging.getLogger(__name__)

class BlogScraper:
    def __init__(self):
        self.session = requests.Session()
        self.visited_urls = set()
        self._configure_session()
        self._validate_base_url()

    def _configure_session(self):
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9"
        })

    def _validate_base_url(self):
        parsed = urlparse(BASE_URL)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"URL base inválida: {BASE_URL}")

    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            time.sleep(random.uniform(*REQUEST_DELAY))
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            logger.error(f"Error obteniendo {url}: {type(e).__name__}")
            return None

    def get_all_article_links(self) -> List[str]:
        all_links = set()
        current_url = BASE_URL
        page_count = 0

        while page_count < MAX_PAGES:
            soup = self._get_soup(current_url)
            if not soup:
                break

            # Extraer enlaces
            new_links = self._extract_links(soup, current_url)
            all_links.update(new_links)
            logger.info(f"Página {page_count + 1}: {len(new_links)} enlaces")

            # Siguiente página
            next_url = self._get_next_page(soup, current_url)
            if not next_url or next_url in self.visited_urls:
                break

            self.visited_urls.add(next_url)
            current_url = next_url
            page_count += 1

        return list(all_links)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> set:
        links = set()
        for selector in SELECTORS["article_links"]:
            for link in soup.select(selector):
                if href := link.get('href'):
                    full_url = urljoin(base_url, href)
                    if self._is_valid_url(full_url):
                        links.add(full_url)
        return links

    def _get_next_page(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        for selector in SELECTORS["next_page"]:
            if next_btn := soup.select_one(selector):
                if href := next_btn.get('href'):
                    return urljoin(current_url, href)
        return None

    def _is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return (
            parsed.netloc == urlparse(BASE_URL).netloc and
            parsed.path.strip('/') != '' and
            url not in self.visited_urls
        )

    def extract_articles(self, urls: List[str]) -> List[Dict]:
        return [article for url in urls if (article := self._extract_article(url))]

    def _extract_article(self, url: str) -> Optional[Dict]:
        soup = self._get_soup(url)
        if not soup:
            return None

        try:
            return {
                "title": self._safe_extract(soup, "title"),
                "content": self._safe_extract(soup, "content"),
                "date": self._safe_extract(soup, "date", is_date=True),
                "url": url
            }
        except Exception as e:
            logger.error(f"Error procesando {url}: {str(e)}")
            return None

    def _safe_extract(self, soup: BeautifulSoup, field: str, is_date: bool = False) -> str:
        for selector in SELECTORS.get(field, []):
            if element := soup.select_one(selector):
                if is_date and 'datetime' in selector:
                    return element.get('datetime', '').strip()
                return element.get_text(separator=' ', strip=True)
        return ""