import os
from dotenv import load_dotenv

load_dotenv(".dev.env")
# load_dotenv(".prod.env")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL")
# MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
