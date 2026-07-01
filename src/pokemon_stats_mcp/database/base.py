from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import pandas as pd

class DatabaseAdapter(ABC):
    """Abstract Base Class for relational/denormalized database adapters."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        pass
        
    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass
        
    @abstractmethod
    def create_table(self, table_name: str) -> None:
        """Create a table in the staging schema with id, name, data (JSON)."""
        pass
        
    @abstractmethod
    def insert_or_replace(self, table_name: str, item_id: int, name: Optional[str], data: Dict[str, Any]) -> None:
        """Insert or replace a row in the specified staging table."""
        pass
        
    @abstractmethod
    def find_by_id(self, table_name: str, item_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a row by its primary key ID from the staging table."""
        pass
        
    @abstractmethod
    def find_by_name(self, table_name: str, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a row by its name from the staging table."""
        pass
        
    @abstractmethod
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """Execute a raw SQL query and return a Pandas DataFrame."""
        pass
