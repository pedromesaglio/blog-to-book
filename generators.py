"""
Módulo para generar libros en diferentes formatos.
"""
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List, Dict
import logging
from config import PDF_CONFIG

logger = logging.getLogger(__name__)

class BookGenerator:
    """Clase base para generadores de libros."""
    
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
    
    def generate(self):
        raise NotImplementedError("Método debe ser implementado en subclases")

class DocxGenerator(BookGenerator):
    """Genera archivo DOCX."""
    
    def generate(self):
        doc = Document()
        for article in self.articles:
            doc.add_heading(article["title"], level=1)
            doc.add_paragraph(f"Fecha: {article['date']}", style="Intense Quote")
            doc.add_paragraph(article["content"])
            doc.add_page_break()
        doc.save(self.filename)
        logger.info(f"DOCX generado: {self.filename}")

class PdfGenerator(BookGenerator):
    """Genera archivo PDF."""
    
    def generate(self):
        cfg = PDF_CONFIG
        c = canvas.Canvas(self.filename, pagesize=letter)
        y_position = 750
        for article in self.articles:
            # Título
            c.setFont(cfg["font_bold"], cfg["font_size"] + 2)
            c.drawString(50, y_position, article["title"])
            y_position -= 30
            
            # Fecha
            c.setFont(cfg["font_regular"], cfg["font_size"] - 2)
            c.drawString(50, y_position, f"Publicado el: {article['date']}")
            y_position -= 20
            
            # Contenido
            c.setFont(cfg["font_regular"], cfg["font_size"])
            text = article["content"].split()
            line = []
            for word in text:
                if c.stringWidth(" ".join(line + [word])) < 500:
                    line.append(word)
                else:
                    c.drawString(50, y_position, " ".join(line))
                    y_position -= 15
                    line = [word]
                if y_position < 50:
                    c.showPage()
                    y_position = 750
            if line:
                c.drawString(50, y_position, " ".join(line))
                y_position -= 15
            
            c.showPage()
            y_position = 750
        
        c.save()
        logger.info(f"PDF generado: {self.filename}")