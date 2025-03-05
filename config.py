# Configuración Principal
BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "libro_blog"

SELECTORS = {
    "article_links": "article.latest-posts-list h4 a",
    "title": "h4 a", 
    "content": "div.post-description",
    
    # Selector de fecha mejorado (solo para artículos):
    "date": "article.latest-posts-list span.item-metadata.posts-date a",
    
    "next_page": "a.next.page-numbers"
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