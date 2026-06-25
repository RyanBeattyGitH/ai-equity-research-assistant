from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from .base import Base

class EarningsCall(Base):
    __tablename__ = "earnings_calls"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    quarter = Column(String)
    transcript = Column(Text)
    call_date = Column(DateTime, default=datetime.utcnow)
