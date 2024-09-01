from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from schemas import ChatMessageCreateSchema

from models import User

class ChatService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    async def create_message(chat: ChatMessageCreateSchema):
        
        return
