from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.auth import Token
from app.utils.audit import log_action
from app.db.session import get_db

router = APIRouter(prefix="/api", tags=["auth"])

# Hardcoded users
users_db = {
    "admin@example.com": {
        "username": "admin@example.com",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin"
    },
    "john@example.com": {
        "username": "john@example.com",
        "hashed_password": get_password_hash("share123"),
        "role": "shareholder"
    }
}

@router.post("/token/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]}, expires_delta=access_token_expires)
    db = Session = Depends(get_db)
    log_action(db, user.id, "User logged in")

    return {"access_token": access_token, "token_type": "bearer"}
