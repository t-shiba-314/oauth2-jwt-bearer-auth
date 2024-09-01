import os
import uuid
import shutil

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from models import File, User
from schemas import FileDeleteResponseSchema
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

UPLOAD_DIR = 'uploads'
ORIGINAL_DIR = os.path.join(UPLOAD_DIR, "original")
VECTOR_DIR = os.path.join(UPLOAD_DIR, "vector")

class FileService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def get_file_by_id(self, file_id):
        return self.db.query(File).filter(File.id == file_id).first()

    def get_file_list(self):
        return self.db.query(File).filter(File.created_by == self.current_user.id).all()

    async def create_file(self, file: UploadFile):
        unique_filename = f'{uuid.uuid4()}_{file.filename}'

        original_file_path = self.get_original_file_path(self.current_user.id, file.filename)
        vector_path = self.get_vector_dir_path(self.current_user.id)

        for dir_path in [os.path.dirname(original_file_path), os.path.dirname(vector_path)]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        try:
            contents = await file.read()
            with open(original_file_path, 'wb') as f:
                f.write(contents)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Failed to save file {str(e)}'
            )

        db_file = File(
            filename=unique_filename,
            file_size=len(contents),
            mime_type=file.content_type,
            created_by=self.current_user.id
        )

        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)

        try:
            self.create_and_update_index(original_file_path, vector_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Failed to create index {str(e)}'
            )

        return db_file

    async def delete_file(self, file_id: int):
        file = self.get_file_by_id(file_id=file_id)
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'File with id {file_id} not found'
            )

        if file.created_by != self.current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this file"
            )

        original_file_path = self.get_original_file_path(file.created_by, file.filename)
        vector_path = self.get_vector_dir_path(file.created_by)

        try:
            self.delete_index(original_file_path, vector_path)
        except OSError as e:
            print(f"Warning: Error deleting vector file {vector_path}: {str(e)}")

        try:
            os.remove(original_file_path)
        except OSError as e:
            print(f"Warning: Error deleting file {file.file_path}: {str(e)}")

        original_dir = os.path.dirname(original_file_path)
        if os.path.exists(original_dir) and not os.listdir(original_dir):
            try:
                os.rmdir(original_dir)
                shutil.rmtree(vector_path)
            except OSError as e:
                print(f"Warning: Error removing directory or file: {str(e)}")

        self.db.delete(file)
        self.db.commit()

        return FileDeleteResponseSchema(message="File deleted successfully")

    def get_original_file_path(self, user_id: int, filename: str):
        return os.path.join(ORIGINAL_DIR, str(user_id), filename)

    def get_vector_dir_path(self, user_id: int):
        return os.path.join(VECTOR_DIR, str(user_id))

    def create_and_update_index(self, original_file_path: str, vector_path: str):
        documents = SimpleDirectoryReader(input_files=[original_file_path], filename_as_id=True).load_data()

        if os.path.exists(vector_path):
            storage_context = StorageContext.from_defaults(persist_dir=vector_path)
            index = load_index_from_storage(storage_context)
            for doc in documents:
                index.insert(doc)
        else:
            sentence_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
            embed_model = OpenAIEmbedding(
                model='text-embedding-3-large',
                api_key=OPENAI_API_KEY
            )
            service_context = ServiceContext.from_defaults(
                node_parser=sentence_splitter,
                embed_model=embed_model
            )
            index = VectorStoreIndex.from_documents(
                documents,
                service_context=service_context
            )

        index.storage_context.persist(persist_dir=vector_path)

        return index

    def delete_index(self, original_file_path: str, vector_path: str):
        storage_context = StorageContext.from_defaults(persist_dir=vector_path)
        index = load_index_from_storage(storage_context)
        for doc_id in list(index.ref_doc_info.keys()):
            if original_file_path in doc_id:
                index.delete_ref_doc(doc_id, delete_from_docstore=True)

        index.storage_context.persist(persist_dir=vector_path)
        return index
