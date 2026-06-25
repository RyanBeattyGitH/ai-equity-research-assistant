from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ticker = Column(String, unique=True, index=True, nullable=False)
    sector = Column(String)
    market_cap = Column(Float)
