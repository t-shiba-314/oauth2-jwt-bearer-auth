from fastapi import FastAPI, APIRouter
from database import engine, Base
from routers import user, file, chat

# api
app = FastAPI()
api_router = APIRouter(prefix='/api')
api_router.include_router(user.router)
api_router.include_router(file.router)
api_router.include_router(chat.router)

app.include_router(api_router)

# database
Base.metadata.create_all(bind=engine)
