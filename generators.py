from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Image, Table, TableStyle, Frame, PageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor, Inches
from typing import List, Dict
import logging
from datetime import datetime
from config import PDF_CONFIG
import os

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
        self.styles = self._create_styles()
        self.logo = self._get_logo()

    def _get_logo(self):
        if os.path.exists(PDF_CONFIG["branding"]["logo_path"]):
            return Image(PDF_CONFIG["branding"]["logo_path"], width=40*mm, height=12*mm)
        return None

    def _create_styles(self):
        return {
            'title': ParagraphStyle(
                name='Title',
                fontName=PDF_CONFIG["fonts"]["bold"],
                fontSize=PDF_CONFIG["fonts"]["sizes"]["title"],
                textColor=colors.HexColor(PDF_CONFIG["colors"]["primary"]),
                spaceAfter=14,
                alignment=1
            ),
            'date': ParagraphStyle(
                name='Date',
                fontName=PDF_CONFIG["fonts"]["italic"],
                fontSize=PDF_CONFIG["fonts"]["sizes"]["subtitle"],
                textColor=colors.HexColor(PDF_CONFIG["colors"]["secondary"]),
                spaceAfter=10
            ),
            'content': ParagraphStyle(
                name='Content',
                fontName=PDF_CONFIG["fonts"]["regular"],
                fontSize=PDF_CONFIG["fonts"]["sizes"]["body"],
                leading=PDF_CONFIG["fonts"]["sizes"]["body"] * 1.5,
                textColor=colors.HexColor(PDF_CONFIG["colors"]["text"])
            )
        }

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        # Header
        if self.logo:
            self.logo.drawOn(canvas, 30*mm, A4[1] - 30*mm)
        # Footer
        footer_text = f"Página {doc.page} | {datetime.now().strftime('%d/%m/%Y')}"
        canvas.setFont(PDF_CONFIG["fonts"]["regular"], PDF_CONFIG["fonts"]["sizes"]["footer"])
        canvas.drawString(30*mm, 20*mm, footer_text)
        canvas.restoreState()

    def generate(self):
        try:
            doc = SimpleDocTemplate(
                self.filename,
                pagesize=A4,
                leftMargin=PDF_CONFIG["page"]["margin"]["left"] * mm,
                rightMargin=PDF_CONFIG["page"]["margin"]["right"] * mm,
                topMargin=PDF_CONFIG["page"]["margin"]["top"] * mm,
                bottomMargin=PDF_CONFIG["page"]["margin"]["bottom"] * mm
            )
            
            elements = [
                Paragraph("Catálogo de Artículos", self.styles['title']),
                Spacer(1, 20)
            ]
            
            for article in self.articles:
                elements += [
                    Paragraph(article["title"], self.styles['title']),
                    Paragraph(f'Publicado el {article["date"]}', self.styles['date']),
                    Spacer(1, 10),
                    Paragraph(article["content"], self.styles['content']),
                    PageBreak()
                ]
            
            doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
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
            
            # Portada
            doc.add_heading('Catálogo de Artículos', 0)
            doc.add_paragraph().add_run('Edición Especial').italic = True
            
            # Contenido
            for article in self.articles:
                doc.add_heading(article['title'], level=1)
                doc.add_paragraph(f"Publicado el {article['date']}", style='Intense Quote')
                doc.add_paragraph(article['content'])
                doc.add_page_break()
            
            doc.save(self.filename)
            logger.info(f"DOCX generado: {self.filename}")
        
        except Exception as e:
            logger.error(f"Error generando DOCX: {str(e)}")
            raise
    
    def _setup_styles(self, doc):
        styles = doc.styles
        # Estilo título
        title_style = styles['Heading 1']
        title_style.font.name = PDF_CONFIG["fonts"]["bold"]
        title_style.font.size = Pt(16)
        title_style.font.color.rgb = RGBColor.from_string(PDF_CONFIG["colors"]["primary"][1:])
        
        # Estilo fecha
        quote_style = styles['Intense Quote']
        quote_style.font.name = PDF_CONFIG["fonts"]["italic"]
        quote_style.font.size = Pt(12)
        quote_style.font.color.rgb = RGBColor.from_string(PDF_CONFIG["colors"]["secondary"][1:])