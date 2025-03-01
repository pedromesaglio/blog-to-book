import argparse
import logging
from dotenv import load_dotenv
from scraper import BlogScraper
from generators import DocxGenerator, PdfGenerator
from uploaders import GoogleDriveUploader, HttpUploader
from config import UPLOAD_SERVICES, OUTPUT_FILENAME

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def main():
    parser = argparse.ArgumentParser(description='📚 Blog to Book Converter')
    parser.add_argument('--format', '-f', choices=['docx', 'pdf'], default='docx')
    parser.add_argument('--output', '-o', default=OUTPUT_FILENAME)
    parser.add_argument('--upload', '-u', choices=['google-drive', 'http'])
    args = parser.parse_args()
    
    try:
        # 1. Scrape content
        scraper = BlogScraper()
        articles = [art for art in (
            scraper.extract_article(url) 
            for url in scraper.get_article_links()
        ) if art]
        
        # 2. Generate book
        ext = args.format
        filename = f"{args.output}.{ext}"
        
        if ext == 'docx':
            generator = DocxGenerator(articles, filename)
        else:
            generator = PdfGenerator(articles, filename)
            
        generator.generate()
        
        # 3. Upload
        if args.upload:
            service_config = UPLOAD_SERVICES[args.upload]
            if args.upload == 'google-drive':
                uploader = GoogleDriveUploader(service_config)
            else:
                uploader = HttpUploader(service_config)
                
            link = uploader.upload(filename)
            logging.info(f"🔗 Access your book here: {link}")
            
    except Exception as e:
        logging.error(f"💥 Critical error: {str(e)}", exc_info=True)
        exit(1)

if __name__ == '__main__':
    main()