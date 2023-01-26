import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

postgres = create_engine(f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:5432/{os.getenv('DBNAME')}")

cur = postgres.connect()