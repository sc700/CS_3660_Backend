from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)