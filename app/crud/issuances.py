from sqlalchemy.orm import Session
from app.models.issuance import ShareIssuance
from app.models.shareholder import ShareholderProfile
from app.schemas.issuance import IssuanceCreate
from sqlalchemy.orm import Session
from sqlalchemy import func


def create_issuance(db: Session, issuance: IssuanceCreate):
    shareholder = db.query(ShareholderProfile).filter_by(id=issuance.shareholder_id).first()
    if not shareholder:
        return None
    new_issuance = ShareIssuance(
        shareholder_id=issuance.shareholder_id,
        number_of_shares=issuance.number_of_shares,
        price_per_share=issuance.price_per_share
    )
    db.add(new_issuance)
    db.commit()
    db.refresh(new_issuance)
    return new_issuance

def get_issuances_for_admin(db: Session):
    return db.query(ShareIssuance).all()

def get_issuances_for_shareholder(db: Session, shareholder_id: int):
    return db.query(ShareIssuance).filter_by(shareholder_id=shareholder_id).all()

def get_ownership_distribution(db: Session):
    # Sum all shares
    total_shares = db.query(func.sum(ShareIssuance.number_of_shares)).scalar() or 0
    if total_shares == 0:
        return []

    # Get each shareholder's total shares
    results = (
        db.query(ShareholderProfile.name, func.sum(ShareIssuance.number_of_shares).label("shares"))
        .join(ShareIssuance, ShareIssuance.shareholder_id == ShareholderProfile.id)
        .group_by(ShareholderProfile.id)
        .all()
    )

    distribution = []
    for name, shares in results:
        percentage = (shares / total_shares) * 100
        distribution.append({
            "name": name,
            "shares": shares,
            "percentage": round(percentage, 2)
        })
    return distribution
