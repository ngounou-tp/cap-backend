from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.issuance import IssuanceCreate, Issuance
from app.crud import issuances
from app.models.shareholder import ShareholderProfile
from app.core.deps import get_current_user
from typing import List
from app.utils.pdf_generator import generate_certificate
from fastapi.responses import StreamingResponse
from app.utils.audit import log_action
from app.utils.email import send_email



router = APIRouter(prefix="/api/issuances", tags=["issuances"])

@router.get("/", response_model=List[Issuance])
def list_issuances(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] == "admin":
        return issuances.get_issuances_for_admin(db)
    
    elif current_user["role"] == "shareholder":
        shareholder = db.query(ShareholderProfile).filter(ShareholderProfile.user_id == current_user["sub"]).first()
        if not shareholder:
            raise HTTPException(status_code=404, detail="Shareholder profile not found")
        return issuances.get_issuances_for_shareholder(db, shareholder.id)
    
    raise HTTPException(status_code=403, detail="Not authorized")


@router.post("/", response_model=Issuance)
def create_issuance(data: IssuanceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can issue shares")
    
    if data.number_of_shares <= 0:
        raise HTTPException(status_code=400, detail="Number of shares must be greater than 0")
    
    if data.price_per_share <= 0:
        raise HTTPException(status_code=400, detail="Price per share must be greater than 0")
    
    issuance = issuances.create_issuance(db, data)
    if not issuance:
        raise HTTPException(status_code=404, detail="Shareholder not found")
    log_action(db, current_user["sub"], f"Issuance created for shareholder {data.shareholder_id}")
    send_email(data.email, "New Share Issuance", f"You have received {data.number_of_shares} shares.")
    
    return issuance

@router.get("/{id}/certificate")
def get_certificate(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    issuance = db.query(Issuance).filter(Issuance.id == id).first()
    if not issuance:
        raise HTTPException(status_code=404, detail="Issuance not found")

    shareholder = db.query(ShareholderProfile).filter(ShareholderProfile.id == issuance.shareholder_id).first()
    if not shareholder:
        raise HTTPException(status_code=404, detail="Shareholder not found")

    if current_user["role"] != "admin" and current_user["sub"] != shareholder.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    pdf_buffer = generate_certificate(issuance, shareholder)
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=certificate.pdf"})

@router.get("/distribution/")
def get_distribution(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return issuances.get_ownership_distribution(db)

