from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from docx import Document
from typing import List, Dict
import logging
from config import PDF_CONFIG

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
        self.styles = self._create_styles()

    def _create_styles(self):
        styles = getSampleStyleSheet()
        styles.add({
            "Title": self._build_style(
                font=PDF_CONFIG["fonts"]["bold"],
                size=PDF_CONFIG["fonts"]["sizes"]["title"],
                space_after=10
            ),
            "Subtitle": self._build_style(
                font=PDF_CONFIG["fonts"]["regular"],
                size=PDF_CONFIG["fonts"]["sizes"]["subtitle"],
                color=colors.grey
            ),
            "Body": self._build_style(
                font=PDF_CONFIG["fonts"]["regular"],
                size=PDF_CONFIG["fonts"]["sizes"]["body"]
            )
        })
        return styles

    def _build_style(self, **kwargs):
        return {
            "fontName": kwargs.get("font", "Helvetica"),
            "fontSize": kwargs.get("size", 12),
            "leading": kwargs.get("size", 12) * PDF_CONFIG["styles"]["line_height"],
            "spaceAfter": kwargs.get("space_after", PDF_CONFIG["styles"]["paragraph_spacing"]),
            "textColor": kwargs.get("color", colors.black)
        }

    def generate(self):
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            **{k: v for k, v in PDF_CONFIG["page"]["margins"].items()}
        )
        
        elements = []
        for article in self.articles:
            elements += [
                Paragraph(article.get("title", "Sin título"), self.styles["Title"]),
                Paragraph(f"Publicado el: {article.get('date', 'Fecha desconocida')}", self.styles["Subtitle"]),
                Spacer(1, 15),
                Paragraph(article.get("content", ""), self.styles["Body"]),
                Spacer(1, 30)
            ]
        
        doc.build(elements)
        logger.info(f"PDF generado: {self.filename}")


class DOCXGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename

    def generate(self):
        doc = Document()
        self._setup_styles(doc)
        
        for article in self.articles:
            self._add_article(doc, article)
        
        try:
            doc.save(self.filename)
            logger.info(f"DOCX generado: {self.filename}")
        except Exception as e:
            logger.error(f"Error guardando DOCX: {str(e)}")

    def _setup_styles(self, doc):
        styles = doc.styles
        if "Quote" not in styles:
            style = styles.add_style("Quote", styles["Intense Quote"])
            style.font.size = 11
            style.font.color.rgb = 0x404040

    def _add_article(self, doc, article: Dict):
        doc.add_heading(article.get("title", "Sin título"), level=1)
        doc.add_paragraph(article.get("date", "Fecha desconocida"), style="Quote")
        doc.add_paragraph(article.get("content", ""))
        doc.add_page_break()