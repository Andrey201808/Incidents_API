import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER ="postgres"
DB_PASSWORD = "pGa20_Dm25!_99"
DB_HOST = "localhost"
DB_PORT = "8000"
DB_NAME = "Incidents"

DATABASE_URL=postgresql://DB_USER:DB_PASSWORD@@{DB_HOST}:{DB_PORT}/{DB_NAME}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
