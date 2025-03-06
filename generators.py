from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from docx import Document
from docx.shared import Pt
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
        cfg = PDF_CONFIG
        
        margin_left = cfg["page"]["margin"]["left"] * 2.83465  # mm to points
        margin_right = cfg["page"]["margin"]["right"] * 2.83465
        
        styles.add(ParagraphStyle(
            name='TitleStyle',
            fontName=cfg["fonts"]["bold"],
            fontSize=cfg["fonts"]["sizes"]["title"],
            leading=cfg["fonts"]["sizes"]["title"] * 1.2,
            textColor=colors.black,
            spaceAfter=20,
            leftIndent=margin_left,
            rightIndent=margin_right
        ))
        
        styles.add(ParagraphStyle(
            name='BodyStyle',
            fontName=cfg["fonts"]["regular"],
            fontSize=cfg["fonts"]["sizes"]["body"],
            leading=cfg["fonts"]["sizes"]["body"] * 1.5,
            textColor=colors.black,
            spaceBefore=10,
            leftIndent=margin_left,
            rightIndent=margin_right
        ))
        
        return styles

    def generate(self):
        try:
            doc = SimpleDocTemplate(
                self.filename,
                pagesize=A4,
                leftMargin=0,
                rightMargin=0,
                topMargin=0,
                bottomMargin=0
            )
            
            elements = []
            for article in self.articles:
                elements += [
                    Paragraph(article["title"], self.styles['TitleStyle']),
                    Paragraph(f'<font color="#666666">{article["date"]}</font>', self.styles['BodyStyle']),
                    Spacer(1, 15),
                    Paragraph(article["content"], self.styles['BodyStyle']),
                    PageBreak()
                ]
            
            doc.build(elements)
            logger.info(f"PDF generado: {self.filename}")
        
        except Exception as e:
            logger.error(f"Error generando PDF: {str(e)}")
            raise

class DOCXGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
    
    def generate(self):
        try:
            doc = Document()
            self._setup_styles(doc)
            
            for article in self.articles:
                doc.add_heading(article["title"], level=1)
                doc.add_paragraph(article["date"], style="Quote")
                doc.add_paragraph(article["content"])
                doc.add_page_break()
            
            doc.save(self.filename)
            logger.info(f"DOCX generado: {self.filename}")
        
        except Exception as e:
            logger.error(f"Error generando DOCX: {str(e)}")
            raise
    
    def _setup_styles(self, doc):
        styles = doc.styles
        if "Quote" not in styles:
            style = styles.add_style("Quote", styles["Intense Quote"])
            font = style.font
            font.size = Pt(11)
            font.color.rgb = 0x404040