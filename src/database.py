from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings


Base = declarative_base()

engine = create_engine(
    settings.sql_alchemy_database_url,
    connect_args={'check_same_thread': False} #needed only for sqlite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def initialize_db():
    Base.metadata.create_all(bind=engine)

def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
