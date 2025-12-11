from abc import ABC, abstractmethod
from typing import List, Optional
from models.db_schemes import RetrievedDocument

class VectorDBInterface(ABC):
    
    @abstractmethod
    async def connect(self):
        pass
    
    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    async def list_all_collections(self) -> List:
        pass
    
    @abstractmethod
    async def get_collection_info(self, collection_name: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def delete_collection(self, collection_name: str):
        pass
    
    @abstractmethod
    async def create_collection(self, collection_name: str,
                                embedding_size: int,
                                do_reset: bool = False):
        pass
    
    @abstractmethod
    async def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: Optional[dict] = None,
                         record_id: Optional[str] = None) -> bool:
        pass
    
    @abstractmethod
    async def insert_many(self, collection_name: str, texts: list, vectors: list,
                          metadata: Optional[list] = None,
                          record_ids: Optional[list] = None,
                          batch_size: int = 50) -> bool:
        pass
    
    @abstractmethod
    async def search_by_vector(self, collection_name: str, vector: list, limit: int) -> Optional[List[RetrievedDocument]]:
        pass
