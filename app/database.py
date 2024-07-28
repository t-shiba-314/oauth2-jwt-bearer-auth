import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db/{os.getenv('DB_NAME')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLoacal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
