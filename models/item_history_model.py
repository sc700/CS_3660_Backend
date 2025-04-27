from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base_model import Base

class ItemHistory(Base):
    __tablename__ = "item_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"))
    timestamp = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)

    item = relationship("Item", back_populates="history")