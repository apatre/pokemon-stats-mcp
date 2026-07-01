from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class VectorDatabaseAdapter(ABC):
    """Abstract Base Class for vector database adapters (future implementation)."""
    
    @abstractmethod
    def connect(self) -> None:
        pass
        
    @abstractmethod
    def close(self) -> None:
        pass
        
    @abstractmethod
    def insert_vector(self, collection_name: str, vector_id: str, vector: List[float], payload: Dict[str, Any]) -> None:
        """Store a vector embedding and its associated payload/metadata."""
        pass
        
    @abstractmethod
    def search_similarity(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for vector records similar to the query vector."""
        pass
