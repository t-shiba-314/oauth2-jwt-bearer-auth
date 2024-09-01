from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_chat_service
from schemas import ChatMessageOutSchema, ChatMessageCreateSchema, ChatConversationListOutSchema, ChatConversationOutSchema
from services import ChatService

router = APIRouter(tags=['chats'], prefix='/chat')

@router.post('/message', response_model=ChatMessageOutSchema)
async def create_message(chat: ChatMessageCreateSchema, chat_service: ChatService = Depends(get_chat_service)):
    response = await chat_service.create_message(chat=chat)
    return ChatMessageOutSchema.model_validate(response)

@router.get('/conversations', response_model=ChatConversationListOutSchema)
def get_conversations(chat_service: ChatService = Depends(get_chat_service)):
    return

@router.get('/conversations/{conversation_id}', response_model=ChatConversationOutSchema)
def get_conversation(conversation_id: int, chat_service: ChatService = Depends(get_chat_service)):
    return
