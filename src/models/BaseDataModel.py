from helpers.config import Settings, get_settings
from sqlalchemy.ext.asyncio import async_sessionmaker

class BaseDataModel:
    
    def __init__(self, db_client: async_sessionmaker):
        self.db_client = db_client
        self.app_settings = get_settings()
