import argparse
import logging
import sys
from scraper import BlogScraper
from generators import PDFGenerator, DOCXGenerator

def main():
    parser = argparse.ArgumentParser(description="📚 Conversor de Blog a Libro")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    parser.add_argument("-o", "--output", default="libro_blog")
    parser.add_argument("--max-articles", type=int, help="Límite máximo de artículos")
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
        urls = scraper.get_all_article_links(args.max_articles)
        logger.info(f"✅ Encontrados {len(urls)} URLs")
        
        logger.info("⚙️ Procesando contenido...")
        articles = scraper.extract_articles(urls)
        
        # Validación crítica
        required_keys = ["title", "content", "date"]
        for art in articles:
            if not all(art.get(key) for key in required_keys) or len(art["content"]) < 100:
                logger.error(f"❌ Artículo inválido: {art.get('url', 'Sin URL')}")
                sys.exit(1)
        
        logger.info(f"📚 Artículos válidos: {len(articles)}")
        
        logger.info(f"🖨️ Generando {args.format.upper()}...")
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