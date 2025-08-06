from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class ShareholderProfile(Base):
    __tablename__ = "shareholders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    email = Column(String, unique=True, nullable=False)
    user = relationship("User", backref="shareholder_profile")
    issuances = relationship("ShareIssuance", back_populates="shareholder")
