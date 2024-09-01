from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class ChatConversationOutSchema(BaseModel):
    pass

class ChatConversationListOutSchema(BaseModel):
    pass

class ChatMessageOutSchema(BaseModel):
    message_id: int
    thread_id: int
    user_id: int
    bot_response: str

    model_config = ConfigDict(from_attributes=True)


class ChatMessageCreateSchema(BaseModel):
    user_id: int
    thread_id: Optional[int]
    message: str
