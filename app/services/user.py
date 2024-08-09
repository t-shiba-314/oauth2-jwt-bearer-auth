from sqlalchemy.orm import Session
from models import User
from schemas import UserCreateSchema
from auth import get_password_hash, decode_token
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return  self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user: UserCreateSchema):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def reset_password(self, token: str, new_password: str):
        payload = decode_token(token)
        if payload is None:
            return False
        
        email = payload.get('sub')
        if email is None:
            return False
        
        exp = payload.get('exp')
        if exp is None or datetime.utcfromtimestamp(exp) < datetime.utcnow():
            return False
        
        user = self.get_user_by_email(email)
        if user is None:
            return False
        
        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password
        self.db.commit()
        return True
    
    