from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings
from typing import AsyncGenerator
from sqlalchemy import create_engine



# Create the async engine using your database URL
async_engine = create_async_engine(settings.database_url, echo=True)

# Create a sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class DatabaseFactory:
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db: Session = None

    def close_session(self):
        self.db.close()

    def get_session(self):
        if not self.db or not self.db.is_active:
            self.db = self.SessionLocal()
            
        return self.db 
