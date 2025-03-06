from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    publish_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class DatabaseManager:
    def __init__(self, db_name='articles.db'):
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def save_article(self, article_data):
        session = self.Session()
        try:
            # Manejo mejorado de fechas
            publish_date = None
            if article_data.get('date'):
                try:
                    if isinstance(article_data['date'], str):
                        publish_date = datetime.fromisoformat(article_data['date'])
                    else:
                        publish_date = article_data['date']
                except Exception as e:
                    logger.warning(f"Error parseando fecha: {str(e)}")
            
            article = Article(
                title=article_data['title'],
                content=article_data['content'],
                url=article_data['url'],
                publish_date=publish_date
            )
            session.add(article)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Los demás métodos se mantienen igual...
    def get_all_articles(self):
        session = self.Session()
        try:
            return [{
                'title': art.title,
                'content': art.content,
                'url': art.url,
                'date': art.publish_date.strftime('%Y-%m-%d') if art.publish_date else 'Sin fecha'
            } for art in session.query(Article).all()]
        finally:
            session.close()
    
    def article_exists(self, url):
        session = self.Session()
        try:
            return session.query(Article).filter_by(url=url).count() > 0
        finally:
            session.close()