from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.shareholder import ShareholderProfile
from app.core.security import get_password_hash
from app.schemas.shareholder import ShareholderCreate

def create_shareholder(db: Session, shareholder: ShareholderCreate):
    user = User(email=shareholder.email, hashed_password=get_password_hash(shareholder.password), role=UserRole.shareholder)
    db.add(user)
    db.flush()  # To get user.id
    profile = ShareholderProfile(name=shareholder.name, user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_all_shareholders(db: Session):
    shareholders = db.query(ShareholderProfile).all()
    result = []
    for s in shareholders:
        total_shares = sum(i.number_of_shares for i in s.issuances)
        result.append({"id": s.id, "name": s.name, "email": s.user.email, "total_shares": total_shares})
    return result
