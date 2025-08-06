from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class ShareIssuance(Base):
    __tablename__ = "issuances"

    id = Column(Integer, primary_key=True, index=True)
    shareholder_id = Column(Integer, ForeignKey("shareholders.id"))
    number_of_shares = Column(Integer, nullable=False)
    price_per_share = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    shareholder = relationship("ShareholderProfile", back_populates="issuances")
