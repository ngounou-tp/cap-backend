from fastapi import FastAPI
from app.db.session import engine, Base

# Create tables (temporary, will use Alembic later)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cap Table Management API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to Cap Table API"}
