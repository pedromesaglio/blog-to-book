from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List, Dict
import logging
from config import PDF_CONFIG

logger = logging.getLogger(__name__)

class BookGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename

class DocxGenerator(BookGenerator):
    def generate(self):
        doc = Document()
        for article in self.articles:
            doc.add_heading(article['title'], 1)
            doc.add_paragraph(f"📅 {article['date']}", style="Intense Quote")
            doc.add_paragraph(article['content'])
            doc.add_page_break()
        doc.save(self.filename)
        logger.info(f"DOCX generated: {self.filename}")

class PdfGenerator(BookGenerator):
    def generate(self):
        cfg = PDF_CONFIG
        c = canvas.Canvas(self.filename, pagesize=letter)
        y = 750
        margin = 50
        
        for article in self.articles:
            # Title
            c.setFont(cfg['font_bold'], 16)
            title_lines = self._wrap_text(article['title'], 70)
            for line in title_lines:
                c.drawString(margin, y, line)
                y -= 20
                
            # Date
            c.setFont(cfg['font_regular'], 10)
            c.drawString(margin, y-10, f"Publicado el: {article['date']}")
            y -= 30
            
            # Content
            c.setFont(cfg['font_regular'], 12)
            content_lines = self._wrap_text(article['content'], 90)
            for line in content_lines:
                c.drawString(margin, y, line)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = 750
            c.showPage()
            y = 750
            
        c.save()
        logger.info(f"PDF generated: {self.filename}")
    
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