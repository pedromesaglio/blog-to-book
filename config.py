# Configuración mejorada para diseño profesional
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
            "top": 40,
            "bottom": 40,
            "left": 30,
            "right": 30
        }
    },
    "fonts": {
        "regular": "Helvetica",
        "bold": "Helvetica-Bold",
        "italic": "Helvetica-Oblique",
        "sizes": {
            "title": 20,
            "subtitle": 14,
            "body": 11,
            "header": 9,
            "footer": 8
        }
    },
    "colors": {
        "primary": "#2E5BFF",
        "secondary": "#4A4A4A",
        "accent": "#F5F6F7",
        "text": "#2D3A4B"
    },
    "styles": {
        "line_height": 1.5,
        "paragraph_spacing": 12,
        "header_height": 25,
        "footer_height": 15
    },
    "branding": {
        "logo_path": "logo.png",
        "website": "cultivoloco.com.ar"
    }
}