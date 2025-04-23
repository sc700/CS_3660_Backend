from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base

from models.item_history_model import ItemHistory

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    name = Column(String, nullable=False)
    details = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    user = relationship("User", back_populates="items")

    history = relationship(
        "ItemHistory",
        back_populates="item",
        cascade="all, delete-orphan"
    )