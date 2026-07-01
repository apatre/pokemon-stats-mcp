import json
import logging
import duckdb
import pandas as pd
from typing import Any, Dict, Optional
from pokemon_stats_mcp.database.base import DatabaseAdapter

logger = logging.getLogger(__name__)

class DuckDBAdapter(DatabaseAdapter):
    """Concrete implementation of DatabaseAdapter using DuckDB."""
    
    def __init__(self, db_path: str = "data/pokemon_stats.duckdb"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self) -> None:
        if not self.conn:
            self.conn = duckdb.connect(database=self.db_path)
            self.conn.execute("INSTALL json;")
            self.conn.execute("LOAD json;")
            
    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def create_table(self, table_name: str) -> None:
        self.connect()
        self.conn.execute("CREATE SCHEMA IF NOT EXISTS staging")
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS staging.{table_name} (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                data JSON
            )
        """)
        
    def insert_or_replace(self, table_name: str, item_id: int, name: Optional[str], data: Dict[str, Any]) -> None:
        self.connect()
        self.create_table(table_name)
        json_str = json.dumps(data)
        self.conn.execute(
            f"INSERT OR REPLACE INTO staging.{table_name} (id, name, data) VALUES (?, ?, ?)",
            [item_id, name, json_str]
        )
        
    def find_by_id(self, table_name: str, item_id: int) -> Optional[Dict[str, Any]]:
        self.connect()
        self.create_table(table_name)
        row = self.conn.execute(
            f"SELECT data FROM staging.{table_name} WHERE id = ?",
            [item_id]
        ).fetchone()
        if row:
            return json.loads(row[0])
        return None
        
    def find_by_name(self, table_name: str, name: str) -> Optional[Dict[str, Any]]:
        self.connect()
        self.create_table(table_name)
        row = self.conn.execute(
            f"SELECT data FROM staging.{table_name} WHERE name = ?",
            [name.lower().strip()]
        ).fetchone()
        if row:
            return json.loads(row[0])
        return None
        
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        self.connect()
        return self.conn.execute(sql_query).df()
