import os

# Configuración del Blog
BASE_URL = "https://cultivoloco.com.ar/"
OUTPUT_FILENAME = "blog_book"

# Selectores CSS (¡AJUSTAR!)
SELECTORS = {
    "article_links": "a.post-link",
    "title": "h1.entry-title",
    "content": "div.post-content",
    "date": "time.post-date"
}

# Configuración PDF
PDF_CONFIG = {
    "font_size": 12,
    "font_bold": "Helvetica-Bold",
    "font_regular": "Helvetica",
    "page_size": "letter"
}

# Configuración de Subida
UPLOAD_SERVICES = {
    "google-drive": {
        "client_id": os.getenv("GDRIVE_CLIENT_ID"),
        "client_secret": os.getenv("GDRIVE_CLIENT_SECRET"),
        "refresh_token": os.getenv("GDRIVE_REFRESH_TOKEN"),
        "folder_id": os.getenv("GDRIVE_FOLDER_ID", None)
    },
    "http": {
        "api_url": os.getenv("HTTP_UPLOAD_URL"),
        "api_key": os.getenv("HTTP_UPLOAD_KEY")
    }
}