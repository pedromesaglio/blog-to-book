# Configuración del Blog
BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "blog_book"
MAX_WORKERS = 10  # Hilos para procesamiento paralelo
REQUEST_TIMEOUT = 25  # Segundos

# Selectores CSS (¡Ajustar según tu blog!)
SELECTORS = {
    "article_links": "a.post-link",        # Enlaces a artículos
    "title": "h1.post-title",              # Título del artículo
    "content": "div.post-content",         # Contenido principal
    "date": "time.post-date",              # Fecha de publicación
    "next_page": "a.next"                  # Selector de paginación
}

# Configuración PDF
PDF_CONFIG = {
    "page_size": "A4",
    "font_size": 11,
    "title_size": 18,
    "margin": 45,
    "line_height": 15,
    "font_bold": "Helvetica-Bold",
    "font_regular": "Helvetica"
}