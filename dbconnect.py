from sqlalchemy import create_engine,text
import os

from config import settings
from sqlalchemy.orm import sessionmaker


engine = create_engine(str(settings.DATABASE_URL))

#if not settings.PRODUCTION:
#    engine = create_engine(str(settings.DATABASE_DEV_URL))
#else:
#    engine = create_engine(str(settings.DATABASE_PROD_URL))

def get_db_session():
    return sessionmaker(bind=engine)()
    
