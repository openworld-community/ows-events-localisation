from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from root.config import settings

engine = create_engine(settings.DATABASE_URL)

Base = declarative_base()
