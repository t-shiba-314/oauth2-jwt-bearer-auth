from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services import UserService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
