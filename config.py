BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "libro_blog"

# Selectores CSS (¡AJUSTAR ESTOS SEGÚN TU BLOG!)
SELECTORS = {
    "article_links": "a.entry-title",        # Enlaces a artículos
    "title": "h1.entry-title",               # Título del artículo
    "content": "div.entry-content",          # Contenido principal
    "date": "time.entry-date",               # Fecha de publicación
    "next_page": "nav.pagination a.next"     # Paginación (WordPress común)
}

PDF_CONFIG = {
    "page_size": "A4",
    "font_size": 12,
    "title_size": 18,
    "margin": 40,
    "line_height": 14,
    "font_bold": "Helvetica-Bold",
    "font_regular": "Helvetica"
}