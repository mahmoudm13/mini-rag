from .providers import QdrantDBProvider
from .VectorDBInterface import VectorDBInterface
from .VectorDBEnums import VectorDBEnums
from helpers.config import Settings
from controllers.BaseController import BaseController
from typing import Optional

class VectorDBProviderFactory:
    
    def __init__(self, config: Settings):
        self.config = config
        self.base_controller = BaseController()
        
    def create(self, provider: str) -> Optional[VectorDBInterface]:
        
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)
            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECOTR_DB_DISTANCE_METHOD,
            )
        
        return None
