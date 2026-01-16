from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import MYSQL_DATABASE_URL

# Note: Runs only when the db is not created/found
# Sqlite
# sql_engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# MySql Connection
sql_engine = create_engine(
    MYSQL_DATABASE_URL
)

Sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=sql_engine)

Base = declarative_base()
