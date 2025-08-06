from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class ShareIssuance(Base):
    __tablename__ = "share_issuances"

    id = Column(Integer, primary_key=True, index=True)
    shareholder_id = Column(Integer, ForeignKey("shareholder_profiles.id"), nullable=False)
    number_of_shares = Column(Integer, nullable=False)
    price_per_share = Column(Float, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)

    shareholder = relationship("ShareholderProfile", backref="issuances")
