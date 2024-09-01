from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth import verify_token
from database import SessionLocal
from models import User
from services import FileService, UserService, ChatService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token is None:
        return None
    try:
        payload = verify_token(token=token)
        email = payload.get('sub')
        user = db.query(User).filter(User.email == email).first()
        return user
    except HTTPException:
        return None

def get_user_service(
    db: Session = Depends(get_db),
):
    return UserService(
        db=db
    )

def get_file_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return FileService(
        db=db,
        current_user=current_user,
    )

def get_chat_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatService(
        db=db,
        current_user=current_user
    )
