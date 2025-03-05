from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
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
    
    def generate(self):
        try:
            # Configuración de página desde el archivo config
            page_config = PDF_CONFIG["page"]
            fonts_config = PDF_CONFIG["fonts"]
            styles_config = PDF_CONFIG["styles"]
            
            page_size = page_config.get("size", A4)
            margins = page_config.get("margin", {})
            
            c = canvas.Canvas(
                self.filename,
                pagesize=page_size,
                bottomup=1  # Coordenadas desde la parte inferior
            )
            
            # Configurar márgenes
            margin_left = margins.get("left", 40)
            margin_top = margins.get("top", 40)
            
            for article in self.articles:
                self._add_article(
                    c,
                    article,
                    margin_left,
                    margin_top,
                    fonts_config,
                    styles_config
                )
                c.showPage()
            
            c.save()
            logger.info(f"PDF generado: {self.filename}")
        
        except Exception as e:
            logger.error(f"Error generando PDF: {str(e)}")
            raise

    def _add_article(self, c, article: Dict, margin_left: int, margin_top: int, fonts: dict, styles: dict):
        # Configuración inicial
        title = article.get("title", "Sin título")
        date = article.get("date", "Fecha desconocida")
        content = article.get("content", "Contenido no disponible")
        
        # Posicionamiento vertical
        y_position = A4[1] - margin_top  # Altura total - margen superior
        
        # Estilos
        title_font = fonts.get("bold", "Helvetica-Bold")
        title_size = fonts["sizes"].get("title", 18)
        body_font = fonts.get("regular", "Helvetica")
        body_size = fonts["sizes"].get("body", 12)
        line_height = styles.get("line_height", 1.2) * body_size
        
        # Título
        c.setFont(title_font, title_size)
        c.drawString(margin_left, y_position, title[:95])  # Limitar a 95 caracteres
        y_position -= line_height * 2
        
        # Fecha
        c.setFont(body_font, body_size - 2)
        c.drawString(margin_left, y_position - 15, f"Publicado el: {date}")
        y_position -= 30
        
        # Contenido
        c.setFont(body_font, body_size)
        text_object = c.beginText(margin_left, y_position)
        text_object.setLeading(line_height)
        
        # Formatear contenido
        lines = content.split('\n')
        for line in lines:
            text_object.textLine(line.strip())
        
        c.drawText(text_object)

class DOCXGenerator:
    def __init__(self, articles: List[Dict], filename: str):
        self.articles = articles
        self.filename = filename
    
    def generate(self):
        try:
            doc = Document()
            self._setup_styles(doc)
            
            for article in self.articles:
                self._add_article(doc, article)
            
            doc.save(self.filename)
            logger.info(f"DOCX generado: {self.filename}")
        
        except PermissionError:
            logger.error("Error: El archivo está en uso o sin permisos de escritura")
            raise
        except Exception as e:
            logger.error(f"Error generando DOCX: {str(e)}")
            raise
    
    def _setup_styles(self, doc):
        styles = doc.styles
        if "Quote" not in styles:
            quote_style = styles.add_style("Quote", styles["Intense Quote"])
            font = quote_style.font
            font.size = Pt(10)
            font.color.rgb = 0x404040  # Gris oscuro
    
    def _add_article(self, doc, article: Dict):
        # Datos con valores por defecto
        title = article.get("title", "Artículo sin título")
        date = article.get("date", "Fecha no disponible")
        content = article.get("content", "")
        
        # Añadir elementos al documento
        doc.add_heading(title, level=1)
        doc.add_paragraph(date, style="Quote")
        doc.add_paragraph(content)
        doc.add_page_break()