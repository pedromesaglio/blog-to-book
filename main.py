"""
Punto de entrada principal del programa.
"""
import argparse
import logging
from scraper import BlogScraper
from generators import DocxGenerator, PdfGenerator
from config import OUTPUT_FILENAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def main(output_format: str, filename: str):
    # 1. Extraer artículos
    scraper = BlogScraper()
    articles = []
    for link in scraper.get_article_links():
        if article := scraper.extract_article(link):
            articles.append(article)
    logging.info(f"Artículos extraídos: {len(articles)}")
    
    # 2. Generar libro
    if output_format == "docx":
        generator = DocxGenerator(articles, f"{filename}.docx")
    elif output_format == "pdf":
        generator = PdfGenerator(articles, f"{filename}.pdf")
    else:
        raise ValueError("Formato no soportado")
    
    generator.generate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convertir blog a libro")
    parser.add_argument(
        "--format",
        type=str,
        default="docx",
        choices=["docx", "pdf"],
        help="Formato de salida"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=OUTPUT_FILENAME,
        help="Nombre del archivo de salida (sin extensión)"
    )
    args = parser.parse_args()
    
    try:
        main(args.format, args.output)
    except Exception as e:
        logging.error(f"Error en ejecución: {e}", exc_info=True)