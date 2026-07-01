import logging
from typing import Any, Dict, List
from pokemon_stats_mcp.database.vector_adapter import VectorDatabaseAdapter

logger = logging.getLogger(__name__)

class DummyVectorAdapter(VectorDatabaseAdapter):
    """A dummy/placeholder implementation of VectorDatabaseAdapter for future use."""
    
    def __init__(self, provider: str = "chromadb"):
        self.provider = provider
        
    def connect(self) -> None:
        logger.info(f"Vector Database ({self.provider}) adapter connected (mock).")
        
    def close(self) -> None:
        logger.info(f"Vector Database ({self.provider}) adapter closed (mock).")
        
    def insert_vector(self, collection_name: str, vector_id: str, vector: List[float], payload: Dict[str, Any]) -> None:
        logger.info(f"Vector Database: Inserted vector {vector_id} into collection {collection_name} (mock).")
        
    def search_similarity(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Vector Database: Searching collection {collection_name} for top {limit} nearest neighbors (mock).")
        return []
