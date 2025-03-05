BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "cultivoloco_ebook"
MAX_PAGES = 20
REQUEST_DELAY = (1, 3)
MAX_RETRIES = 3

SELECTORS = {
    "article_links": [
        "article.post h2 a",
        "article.latest-post a.entry-title"
    ],
    "title": [
        "h1.entry-title",
        "h1.post-title",
        "h1"
    ],
    "content": [
        "div.entry-content",
        "div.post-content",
        "article.post"
    ],
    "date": [
        "time.entry-date[datetime]",
        "span.post-date",
        "div.post-meta time"
    ],
    "next_page": [
        "a.next.page-numbers",
        "li.pagination-next a"
    ]
}

PDF_CONFIG = {
    "page": {
        "size": "A4",
        "margins": {
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
            "title": 20,
            "subtitle": 14,
            "body": 12
        }
    },
    "styles": {
        "line_height": 1.25,
        "paragraph_spacing": 15
    }
}