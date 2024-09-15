""" This module initializes the database. """
from .db import Base, engine
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database.
    """
    Base.metadata.create_all(bind=engine)
