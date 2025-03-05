# Configuración principal
BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "libro_blog"
MAX_PAGES = 20  # Límite máximo de páginas a scrapear

SELECTORS = {
    # Selectores para listado de artículos
    "article_links": [
        "article.post-item h2 a",
        "article.latest-posts-list h4 a"
    ],
    
    # Selectores dentro de cada artículo
    "title": [
        "h1.entry-title",
        "h1.single-title",
        "h1"
    ],
    "content": [
        "div.entry-content",
        "div.post-content",
        "div.post-description"
    ],
    "date": [
        "time.entry-date[datetime]",
        "span.post-date",
        "span.item-metadata.posts-date a"
    ],
    
    # Selectores de paginación
    "next_page": [
        "a.next.page-numbers",
        "li.next a"
    ]
}

# Configuración PDF (estructura original mejorada)
PDF_CONFIG = {
    "page": {
        "size": "A4",
        "margin": {
            "top": 40,
            "bottom": 40,
            "left": 30,
            "right": 30
        }
    },
    "fonts": {
        "regular": "Helvetica",
        "bold": "Helvetica-Bold",
        "sizes": {
            "title": 18,
            "body": 12
        }
    },
    "styles": {
        "line_height": 1.2,
        "paragraph_spacing": 8
    },
    # Nueva clave para acceso directo
    "page_size": "A4"  
}