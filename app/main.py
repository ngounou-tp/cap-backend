from fastapi import FastAPI
from app.db.session import engine, Base, SessionLocal
from app.api import auth, issuances, shareholders
from app.models.user import User
from app.models.shareholder import ShareholderProfile
from app.core.security import get_password_hash
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cap Table Management API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",  # include both just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             
    allow_credentials=True,
    allow_methods=["*"],                
    allow_headers=["*"],               
)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    admin_email = "admin@example.com"
    shareholder_email = "shareholder@example.com"

    if not db.query(User).filter_by(email=admin_email).first():
        admin = User(email=admin_email, hashed_password=get_password_hash("admin123"), role="admin")
        db.add(admin)
    
    if not db.query(User).filter_by(email=shareholder_email).first():
        shareholder_user = User(email=shareholder_email, hashed_password=get_password_hash("share123"), role="shareholder")
        db.add(shareholder_user)
        db.commit()
        db.refresh(shareholder_user)

        shareholder = ShareholderProfile(user_id=shareholder_user.id, name="John Doe", email=shareholder_email)
        db.add(shareholder)

    db.commit()
    db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Cap Table API"}

app.include_router(auth.router)
app.include_router(shareholders.router)
app.include_router(issuances.router)
