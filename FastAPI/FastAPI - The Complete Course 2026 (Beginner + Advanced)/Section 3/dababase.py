from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Runs only when the db is not created/found
sql_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=sql_engine)

Base = declarative_base()
