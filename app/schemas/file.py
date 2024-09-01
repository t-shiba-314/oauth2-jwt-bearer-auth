from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class FileSchema(BaseModel):
    id: int
    filename: str
    file_size: int
    mime_type: str
    created_at: datetime
    created_by: int

class FileOutSchema(FileSchema):
    model_config = ConfigDict(from_attributes=True)

class FileDeleteResponseSchema(BaseModel):
    message: str

class FileListOutSchema(BaseModel):
    files: List[FileOutSchema]
