from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.shareholder import ShareholderCreate
from app.crud import shareholders
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/shareholders", tags=["shareholders"])

@router.get("/")
def list_shareholders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return shareholders.get_all_shareholders(db)

@router.post("/")
def create_shareholder(data: ShareholderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return shareholders.create_shareholder(db, data)
