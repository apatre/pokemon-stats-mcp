from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TableSchema:
    """Represents a table schema definition"""
    name: str
    columns: Dict[str, str]
    primary_key: Optional[str] = None


class DBModelBase(ABC):
    @abstractmethod
    def create_table(
        self, 
        table_name: str, 
        columns: Dict[str, str], 
        primary_key: Optional[str] = None
    ) -> None:
        """Create a new table in the database."""
        pass

    @abstractmethod
    def drop_table(self, table_name: str) -> None:
        """Drop a table from the database."""
        pass

    @abstractmethod
    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        pass

    @abstractmethod
    def insert(self, table_name: str, data: Dict[str, Any]) -> None:
        """Insert a single row."""
        pass

    @abstractmethod
    def insert_bulk(self, table_name: str, data_list: List[Dict[str, Any]]) -> int:
        """Insert multiple rows efficiently."""
        pass

    @abstractmethod
    def get_all(
        self,
        table_name: str,
        limit: Optional[int] = None,
        offset: int = 0,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all rows with optional pagination and ordering."""
        pass

    @abstractmethod
    def get_by_id(self, table_name: str, id_value: Any, id_column: str = "id") -> Optional[Dict[str, Any]]:
        """Get a single row by ID."""
        pass

    @abstractmethod
    def find(
        self,
        table_name: str,
        filters: Dict[str, Any],
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Find rows matching filters."""
        pass

    @abstractmethod
    def count(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count rows."""
        pass

    @abstractmethod
    def update(self, table_name: str, data: Dict[str, Any], filters: Dict[str, Any]) -> int:
        """Update rows matching filters."""
        pass

    @abstractmethod
    def update_by_id(self, table_name: str, id_value: Any, data: Dict[str, Any]) -> int:
        """Update a row by ID."""
        pass

    @abstractmethod
    def delete(self, table_name: str, filters: Dict[str, Any]) -> int:
        """Delete rows matching filters."""
        pass

    @abstractmethod
    def delete_by_id(self, table_name: str, id_value: Any) -> int:
        """Delete a row by ID."""
        pass

    @abstractmethod
    def begin_transaction(self) -> None:
        """Begin a transaction."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Commit the current transaction."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Rollback the current transaction."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass

    # ==================== CONTEXT MANAGER ====================
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
