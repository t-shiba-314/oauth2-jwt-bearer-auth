from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from dependencies import get_file_service
from schemas import FileOutSchema, FileDeleteResponseSchema, FileListOutSchema
from services import FileService

router = APIRouter(tags=['files'], prefix='/files')

@router.post('/upload', response_model=FileOutSchema)
async def upload_file(file: UploadFile = File(...), file_service: FileService = Depends(get_file_service)):
    uploaded_file = await file_service.create_file(file=file)
    return FileOutSchema.model_validate(uploaded_file)

@router.get('', response_model=FileListOutSchema)
def get_file_list(file_service: FileService = Depends(get_file_service)):
    files = file_service.get_file_list()
    return FileListOutSchema(files=[FileOutSchema.model_validate(file) for file in files])

@router.get('/{file_id}', response_model=FileOutSchema)
async def get_file(file_id: int, file_service: FileService = Depends(get_file_service)):
    file = file_service.get_file_by_id(file_id=file_id)
    return FileOutSchema.model_validate(file)

@router.delete('/{file_id}', response_model=FileDeleteResponseSchema)
async def delete_file(file_id: int, file_service: FileService = Depends(get_file_service)):
    return await file_service.delete_file(file_id=file_id)
