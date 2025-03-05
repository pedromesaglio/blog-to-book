import argparse
import logging
import sys
from scraper import BlogScraper
from generators import PDFGenerator, DOCXGenerator

def main():
    parser = argparse.ArgumentParser(description="📚 Conversor de Blog a Libro")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    parser.add_argument("-o", "--output", default="libro_blog")
    parser.add_argument("--loglevel", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    try:
        logger.info("🚀 Iniciando proceso...")
        scraper = BlogScraper()
        
        logger.info("🔍 Buscando artículos...")
        urls = scraper.get_all_article_links()
        logger.info(f"✅ Encontrados {len(urls)} artículos")
        
        logger.info("⚙️ Extrayendo contenido...")
        articles = scraper.extract_articles(urls)
        
        # Validación añadida (3 líneas específicas)
        if not all(key in article for article in articles for key in ["title", "content"]):
            logger.error("❌ Algunos artículos tienen estructura incorrecta")
            sys.exit(1)
        
        if not articles:
            logger.error("❌ No hay contenido válido para generar")
            sys.exit(1)
            
        logger.info(f"📚 {len(articles)} artículos listos para generar")
        
        generator = PDFGenerator(articles, f"{args.output}.pdf") if args.format == "pdf" \
            else DOCXGenerator(articles, f"{args.output}.docx")
        
        logger.info(f"🛠️ Generando {args.format.upper()}...")
        generator.generate()
        
        logger.info(f"🎉 ¡Libro generado exitosamente! → {args.output}.{args.format}")

    except KeyboardInterrupt:
        logger.error("⛔ Proceso cancelado por el usuario")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Error crítico: {str(e)}", exc_info=args.loglevel == "DEBUG")
        sys.exit(1)

if __name__ == "__main__":
    main()