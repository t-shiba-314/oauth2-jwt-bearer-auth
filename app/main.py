from fastapi import FastAPI, APIRouter
from database import engine, Base
# routing example
# from routers import user

# api
app = FastAPI()
api_router = APIRouter(prefix='/api')
# routing example
# api_router.include_router(user.router)

app.include_router(api_router)

# database
Base.metadata.create_all(bind=engine)
