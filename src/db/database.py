import databases
from sqlalchemy.ext.declarative import declarative_base
from config import settings


database: databases.core.Database = databases.Database(settings.DB_URI)

Base = declarative_base()
