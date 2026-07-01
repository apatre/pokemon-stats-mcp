import logging
import chromadb
from typing import Any, Dict, List, Optional
from pokemon_stats_mcp.database.vector_adapter import VectorDatabaseAdapter

logger = logging.getLogger(__name__)

class ChromaAdapter(VectorDatabaseAdapter):
    """Concrete implementation of VectorDatabaseAdapter using ChromaDB."""
    
    def __init__(self, persist_directory: str = "data/chroma"):
        self.persist_directory = persist_directory
        self.client = None
        
    def connect(self) -> None:
        if not self.client:
            logger.info(f"Connecting to ChromaDB at {self.persist_directory}...")
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
    def close(self) -> None:
        self.client = None
        
    def insert_vector(self, collection_name: str, vector_id: str, vector: List[float], payload: Dict[str, Any]) -> None:
        self.connect()
        collection = self.client.get_or_create_collection(name=collection_name)
        collection.add(
            ids=[vector_id],
            embeddings=[vector],
            metadatas=[payload]
        )
        logger.info(f"ChromaDB: Inserted vector ID '{vector_id}' into collection '{collection_name}'.")
        
    def search_similarity(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        self.connect()
        collection = self.client.get_or_create_collection(name=collection_name)
        
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=limit
        )
        
        formatted_results = []
        if results and "ids" in results and results["ids"]:
            ids = results["ids"][0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]
            
            for idx, item_id in enumerate(ids):
                metadata = metadatas[idx] if idx < len(metadatas) else {}
                distance = distances[idx] if idx < len(distances) else None
                formatted_results.append({
                    "id": item_id,
                    "metadata": metadata,
                    "distance": distance
                })
                
        return formatted_results
