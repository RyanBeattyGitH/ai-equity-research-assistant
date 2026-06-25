from sqlalchemy import Column, Integer, Float, ForeignKey
from .base import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    shares = Column(Float)
    average_price = Column(Float)
