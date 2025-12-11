from .providers import QdrantDBProvider, PGVectorProvider
from .VectorDBInterface import VectorDBInterface
from .VectorDBEnums import VectorDBEnums
from helpers.config import Settings
from controllers.BaseController import BaseController
from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker

class VectorDBProviderFactory:
    
    def __init__(self, config: Settings, db_client: Optional[async_sessionmaker] = None):
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client
        
    def create(self, provider: str) -> Optional[VectorDBInterface]:
        
        if provider == VectorDBEnums.QDRANT.value:
            qdrant_db_client = self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)
            
            return QdrantDBProvider(
                db_client=qdrant_db_client,
                distance_method=self.config.VECOTR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        
        if provider == VectorDBEnums.PGVECTOR.value:
            assert self.db_client, "db_client for PGVector cannot be None"
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECOTR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        
        return None
