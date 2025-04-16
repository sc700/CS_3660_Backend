from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    user = relationship("User", back_populates="items")

    history = relationship("ItemHistory", back_populates="item", cascade="all, delete-orphan")