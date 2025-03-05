# Configuración Principal
BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "libro_blog"

# Selectores CSS Validados para WordPress
SELECTORS = {
    "article_links": "article a[rel='bookmark']",  # Enlaces a artículos
    "title": "h1.entry-title",                     # Título 
    "content": "div.entry-content",                # Contenido
    "date": "time.entry-date",                     # Fecha
    "next_page": "a.next.page-numbers"             # Paginación
}

# Configuración PDF
PDF_CONFIG = {
    "page_size": "A4",
    "font_size": 12,
    "title_size": 18,
    "margin": 40,
    "line_height": 14,
    "font_bold": "Helvetica-Bold",
    "font_regular": "Helvetica"
}