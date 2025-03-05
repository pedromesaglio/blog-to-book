import argparse
import logging
import sys
from pathlib import Path
from scraper import BlogScraper
from generators import PDFGenerator, DOCXGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="📚 Conversor de Blog a Libro")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    parser.add_argument("-o", "--output", default="libro_blog")
    parser.add_argument("--loglevel", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--max-articles", type=int, help="Límite máximo de artículos a procesar")
    args = parser.parse_args()

    logging.getLogger().setLevel(args.loglevel)
    
    try:
        scraper = BlogScraper(delay_range=(1, 2))
        
        logger.info("🔍 Buscando artículos...")
        urls = scraper.get_all_article_links()
        
        if args.max_articles:
            urls = urls[:args.max_articles]
            logger.info(f"⚖️ Límite aplicado: {args.max_articles} artículos")
        
        logger.info(f"✅ Encontrados {len(urls)} artículos")
        
        logger.info("⚙️ Procesando contenido...")
        articles = scraper.extract_articles(urls)
        
        if not articles:
            logger.error("❌ No hay contenido válido para generar")
            sys.exit(1)
            
        logger.info(f"📚 Artículos listos: {len(articles)}")
        
        generator = PDFGenerator(articles, f"{args.output}.pdf") if args.format == "pdf" else DOCXGenerator(articles, f"{args.output}.docx")
        generator.generate()
        
        logger.info(f"🎉 ¡Libro generado! → {args.output}.{args.format}")
        
    except KeyboardInterrupt:
        logger.error("🚫 Operación cancelada por el usuario")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Error crítico: {str(e)}", exc_info=args.loglevel == "DEBUG")
        sys.exit(1)

if __name__ == "__main__":
    main()