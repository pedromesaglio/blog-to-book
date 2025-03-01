from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from docx import Document
from typing import List, Dict
import logging
from config import PDF_CONFIG

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
        self.cfg = PDF_CONFIG
    
    def generate(self):
        c = canvas.Canvas(self.filename, pagesize=A4)
        margin = self.cfg["margin"]
        
        for article in self.articles:
            self._add_article(c, article, margin)
            c.showPage()
        
        c.save()
        logger.info(f"PDF generado: {self.filename}")
    
    def _add_article(self, c, article, margin):
        y_position = A4[1] - margin
        
        # Título
        c.setFont(self.cfg["font_bold"], self.cfg["title_size"])
        title_lines = self._wrap_text(article["title"], 70)
        for line in title_lines:
            y_position = self._check_page(c, y_position, margin)
            c.drawString(margin, y_position, line)
            y_position -= self.cfg["line_height"] + 5
        
        # Fecha
        y_position -= 15
        c.setFont(self.cfg["font_regular"], 10)
        c.drawString(margin, y_position, f"Publicado el: {article['date']}")
        y_position -= 25
        
        # Contenido
        c.setFont(self.cfg["font_regular"], self.cfg["font_size"])
        content_lines = self._wrap_text(article["content"], 100)
        for line in content_lines:
            y_position = self._check_page(c, y_position, margin)
            c.drawString(margin, y_position, line)
            y_position -= self.cfg["line_height"]
    
    def _wrap_text(self, text: str, max_chars: int) -> List[str]:
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            if len(' '.join(current_line + [word])) <= max_chars:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return lines
    
    def _check_page(self, c, y, margin):
        if y < margin + 50:
            c.showPage()
            return A4[1] - margin
        return y

class DOCXGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
    
    def generate(self):
        doc = Document()
        for article in self.articles:
            doc.add_heading(article["title"], level=1)
            doc.add_paragraph(f"📅 {article['date']}", style="Intense Quote")
            doc.add_paragraph(article["content"])
            doc.add_page_break()
        doc.save(self.filename)
        logger.info(f"DOCX generado: {self.filename}")