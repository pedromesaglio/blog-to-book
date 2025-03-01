"""
Configuraciones globales y constantes.
"""

BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "blog_book"

# Headers para requests HTTP
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Selectores CSS (¡AJUSTAR SEGÚN EL BLOG!)
SELECTORS = {
    "article_links": "a.post-link",          # Selector de enlaces a artículos
    "title": "h1.entry-title",               # Selector del título
    "content": "div.post-content",           # Selector del contenido
    "date": "time.post-date"                 # Selector de la fecha
}

# Configuración de PDF
PDF_CONFIG = {
    "font_size": 12,
    "font_bold": "Helvetica-Bold",
    "font_regular": "Helvetica",
    "page_size": "letter"
}