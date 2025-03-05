import argparse
import logging
from scraper import BlogScraper
from generators import PDFGenerator, DOCXGenerator

def main():
    parser = argparse.ArgumentParser(description="📚 Blog to Book Converter")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    parser.add_argument("-o", "--output", default="libro_blog")
    parser.add_argument("--loglevel", default="INFO", choices=["DEBUG", "INFO"])
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=args.loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Iniciando scraper...")
        scraper = BlogScraper()
        
        logger.info("🔍 Buscando artículos...")
        urls = scraper.get_all_article_links()
        logger.info(f"✅ Encontrados: {len(urls)} URLs")
        
        logger.info("⚙️ Procesando contenido...")
        articles = scraper.extract_articles(urls)
        logger.info(f"📚 Artículos válidos: {len(articles)}")
        
        if not articles:
            logger.error("❌ No hay contenido para generar")
            return
        
        logger.info(f"🖨️ Generando {args.format.upper()}...")
        generator = PDFGenerator(articles, f"{args.output}.pdf") if args.format == "pdf" else DOCXGenerator(articles, f"{args.output}.docx")
        generator.generate()
        
        logger.info(f"🎉 ¡Libro generado! Guardado como: {args.output}.{args.format}")
    
    except Exception as e:
        logger.error(f"💥 Error crítico: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()