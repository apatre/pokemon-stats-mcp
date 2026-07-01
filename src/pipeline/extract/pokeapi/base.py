import json
import logging
from typing import Any, Dict, List, Optional
from pokemon_stats_mcp.database import DatabaseAdapter

logger = logging.getLogger(__name__)

class BaseExtractor:
    api_name: str = ""
    table_name: str = ""

    def __init__(self, db_adapter: DatabaseAdapter, client: Optional[Any] = None):
        self.db_adapter = db_adapter
        from .client import PokeAPIClient
        self.client = client or PokeAPIClient()

    def create_table(self) -> None:
        """Create the table in the database."""
        self.db_adapter.create_table(self.table_name)

    def load_item(self, item_data: Dict[str, Any]) -> None:
        """Insert or update a single item's raw JSON data into the table."""
        item_id = item_data.get("id")
        item_name = item_data.get("name")
        self.db_adapter.insert_or_replace(self.table_name, item_id, item_name, item_data)

    def extract_all(self, limit: int = 150) -> None:
        """Fetch all items from PokéAPI and store them in the database."""
        logger.info(f"Extracting all items for api '{self.api_name}' into '{self.table_name}'...")
        self.create_table()
        
        results = self.client.get_list(self.api_name, limit=limit)
        
        for i, item in enumerate(results):
            try:
                details = self.client.get(item["url"])
                self.load_item(details)
                if (i + 1) % 10 == 0 or (i + 1) == len(results):
                    logger.info(f"Loaded {i+1}/{len(results)} items for '{self.api_name}'")
            except Exception as e:
                logger.error(f"Error fetching details for {item.get('name')} from {item.get('url')}: {e}")

    def extract_by_identifier(self, identifier: Any) -> Optional[Dict[str, Any]]:
        """Fetch a single item by its name or ID, store it in the database, and return it."""
        self.create_table()
        
        # Check if already exists in DB
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            data = self.db_adapter.find_by_id(self.table_name, int(identifier))
        else:
            data = self.db_adapter.find_by_name(self.table_name, str(identifier))
            
        if data:
            return data
            
        # If not cached, fetch from PokéAPI
        logger.info(f"Item '{identifier}' not found in '{self.table_name}'. Fetching from PokéAPI...")
        try:
            details = self.client.get(f"{self.api_name}/{identifier}")
            self.load_item(details)
            return details
        except Exception as e:
            logger.error(f"Failed to extract item '{identifier}' from PokéAPI endpoint '{self.api_name}': {e}")
            return None
