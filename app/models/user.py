from sqlalchemy import Column, Integer, String, Enum
from app.db.session import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    shareholder = "shareholder"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
