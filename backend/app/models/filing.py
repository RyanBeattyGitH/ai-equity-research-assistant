from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from .base import Base

class Filing(Base):
    __tablename__ = "filings"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    filing_type = Column(String)  # 10-K, 10-Q
    filing_date = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
