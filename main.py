import argparse
import logging
from scraper import BlogScraper
from generators import PDFGenerator, DOCXGenerator

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("blog_to_book.log"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(description="📘 Conversor de Blog a Libro")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    parser.add_argument("-o", "--output", default="blog_book")
    args = parser.parse_args()
    
    try:
        logger.info("🚀 Iniciando proceso...")
        scraper = BlogScraper()
        
        # Paso 1: Obtener todos los enlaces
        logger.info("🔍 Buscando artículos...")
        urls = scraper.get_all_article_links()
        logger.info(f"📚 Artículos encontrados: {len(urls)}")
        
        # Paso 2: Extraer contenido
        logger.info("⚙️ Procesando artículos...")
        articles = scraper.extract_articles(urls)
        logger.info(f"✅ Artículos válidos: {len(articles)}")
        
        if not articles:
            logger.error("❌ No se encontró contenido válido")
            return
        
        # Paso 3: Generar libro
        logger.info(f"🖨️ Generando {args.format.upper()}...")
        filename = f"{args.output}.{args.format}"
        
        generator = PDFGenerator(articles, filename) if args.format == "pdf" else DOCXGenerator(articles, filename)
        generator.generate()
        
        logger.info(f"🎉 Libro generado: {filename}")
    
    except Exception as e:
        logger.error(f"💥 Error crítico: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()