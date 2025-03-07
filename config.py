BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "libro_blog"
MAX_PAGES = 20

SELECTORS = {
    "article_links": [
        "article.post-item h2 a",
        "article.latest-posts-list h4 a"
    ],
    "title": [
        "h1.entry-title",
        "h1.single-title"
    ],
    "content": [
        "div.entry-content",
        "div.post-content"
    ],
    "date": [
        "time.entry-date[datetime]",
        "span.post-date"
    ],
    "next_page": [
        "a.next.page-numbers",
        "li.next a"
    ]
}

PDF_CONFIG = {
    "page": {
        "size": "A4",
        "margin": {
            "top": 45,
            "bottom": 45,
            "left": 35,
            "right": 35
        }
    },
    "fonts": {
        "heading": "Helvetica-Bold",
        "body": "Helvetica",
        "accent": "Helvetica-Oblique",
        "sizes": {
            "h1": 22,
            "h2": 18,
            "body": 13,
            "meta": 11
        }
    },
    "colors": {
        "primary": "#3A7D44",    # Verde principal
        "secondary": "#6B9F78",  # Verde secundario
        "text": "#000000",       # Texto en negro
        "border": "#8AB894",     # Borde verde
        "background": "#F5FAF6"  # Fondo verde claro
    },
    "spacing": {
        "line_height": 1.6,
        "paragraph": 12,
        "section": 25
    },
    "branding": {
        "logo_path": "logo.png",
        "website": "CultivoLoco.com.ar"
    }
}