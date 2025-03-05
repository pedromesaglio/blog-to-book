from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
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
        self.styles = self._create_styles()

    def _create_styles(self):
        """Crea estilos para el PDF"""
        styles = getSampleStyleSheet()
        styles.add({
            "Title": self._create_style(
                font=self.cfg["fonts"]["bold"],
                size=self.cfg["fonts"]["sizes"]["title"],
                spaceAfter=12
            ),
            "Body": self._create_style(
                font=self.cfg["fonts"]["regular"],
                size=self.cfg["fonts"]["sizes"]["body"]
            )
        })
        return styles

    def _create_style(self, font: str, size: int, **kwargs):
        """Crea un estilo de párrafo"""
        return {
            "fontName": font,
            "fontSize": size,
            "leading": size * self.cfg["styles"]["line_height"],
            "spaceAfter": self.cfg["styles"]["paragraph_spacing"],
            **kwargs
        }

    def generate(self):
        """Genera el archivo PDF"""
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            **self.cfg["page"]["margin"]
        )
        
        elements = []
        for article in self.articles:
            elements += self._build_article_elements(article)
        
        doc.build(elements)
        logger.info(f"PDF generado: {self.filename}")

    def _build_article_elements(self, article: Dict) -> List:
        """Construye los elementos para cada artículo"""
        elements = [
            Paragraph(article.get("title", "Sin título"), self.styles["Title"]),
            Paragraph(f"Publicado el: {article.get('date', 'Fecha desconocida')}", self.styles["Body"]),
            Spacer(1, 12),
            Paragraph(article.get("content", ""), self.styles["Body"]),
            Spacer(1, 24)
        ]
        return elements

class DOCXGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
        self.styles = {
            "title": "Heading1",
            "date": "Quote",
            "content": "Normal"
        }

    def generate(self):
        """Genera el archivo DOCX"""
        doc = Document()
        self._add_custom_styles(doc)
        
        for article in self.articles:
            self._add_article(doc, article)
        
        try:
            doc.save(self.filename)
            logger.info(f"DOCX generado: {self.filename}")
        except PermissionError:
            logger.error("Error: No se puede escribir en el archivo")

    def _add_custom_styles(self, doc):
        """Añade estilos personalizados al documento"""
        styles = doc.styles
        if "Quote" not in styles:
            style = styles.add_style("Quote", styles["Intense Quote"])
            style.font.size = 10
            style.font.italic = True

    def _add_article(self, doc, article: Dict):
        """Añade un artículo al documento"""
        doc.add_heading(article.get("title", "Sin título"), level=1)
        doc.add_paragraph(article.get("date", "Fecha desconocida"), style="Quote")
        doc.add_paragraph(article.get("content", ""))
        doc.add_page_break()