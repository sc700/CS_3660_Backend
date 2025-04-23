from sqlalchemy.orm import sessionmaker, Session
from config import settings
from sqlalchemy import create_engine


class DatabaseFactory:
    def __init__(self):
        try:
            self.engine = create_engine(settings.database_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.db: Session = None
        except Exception as e:
            print(f"Error initializing database connection: {e}")
            raise

    def close_session(self):
        if self.db:
            self.db.close()

    def get_session(self):
        if not self.db or not self.db.is_active:
            self.db = self.SessionLocal()
        return self.db

