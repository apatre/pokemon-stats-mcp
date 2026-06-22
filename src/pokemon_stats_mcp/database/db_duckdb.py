import duckdb
from typing import Any, Dict, List, Optional
from pokemon_stats_mcp.database.db_base import DBModelBase


class DBDuckDBModel(DBModelBase):
    """Comprehensive CRUD class for DuckDB operations implementing DBModelBase"""
    
    def __init__(self, database: str = ":memory:", read_only: bool = False):
        self.database = database
        self.conn = duckdb.connect(database=database, read_only=read_only)
    
    def close(self) -> None:
        self.conn.close()
    
    # ==================== TABLE OPERATIONS ====================
    
    def create_table(
        self, 
        table_name: str, 
        columns: Dict[str, str], 
        primary_key: Optional[str] = None
    ) -> None:
        """Create a table with dict-based column specification"""
        columns_def = []
        for col_name, col_type in columns.items():
            col_def = f"{col_name} {col_type}"
            if primary_key and col_name == primary_key:
                col_def += " PRIMARY KEY"
            columns_def.append(col_def)
        
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_def)})"
        self.conn.execute(sql)
    
    def drop_table(self, table_name: str) -> None:
        self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    def list_tables(self) -> List[str]:
        result = self.conn.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        ).fetchall()
        return [table[0] for table in result]
    
    # ==================== CREATE (INSERT) ====================
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> None:
        """Insert a single row"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
    
    def insert_bulk(self, table_name: str, data_list: List[Dict[str, Any]]) -> int:
        """Insert multiple rows efficiently"""
        if not data_list:
            return 0
        
        columns = list(data_list[0].keys())
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in columns])
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        rows = [list(row.values()) for row in data_list]
        self.conn.executemany(sql, rows)
        return len(rows)
    
    # ==================== READ (SELECT) ====================
    
    def get_all(
        self,
        table_name: str,
        limit: Optional[int] = None,
        offset: int = 0,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all rows with optional pagination and ordering"""
        sql = f"SELECT * FROM {table_name}"
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        
        if limit:
            sql += f" LIMIT {limit}"
            if offset:
                sql += f" OFFSET {offset}"
        
        result = self.conn.execute(sql).fetchall()
        columns = [col[0] for col in self.conn.description]
        return [dict(zip(columns, row)) for row in result]
    
    def get_by_id(self, table_name: str, id_value: Any, id_column: str = "id") -> Optional[Dict[str, Any]]:
        """Get a single row by ID"""
        sql = f"SELECT * FROM {table_name} WHERE {id_column} = ?"
        result = self.conn.execute(sql, [id_value]).fetchone()
        
        if result:
            columns = [col[0] for col in self.conn.description]
            return dict(zip(columns, result))
        return None
    
    def find(
        self,
        table_name: str,
        filters: Dict[str, Any],
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Find rows matching filters"""
        sql = f"SELECT * FROM {table_name}"
        
        if filters:
            conditions = [f"{col} = ?" for col in filters.keys()]
            sql += " WHERE " + " AND ".join(conditions)
        
        if limit:
            sql += f" LIMIT {limit}"
        
        params = list(filters.values()) if filters else []
        result = self.conn.execute(sql, params).fetchall()
        columns = [col[0] for col in self.conn.description]
        return [dict(zip(columns, row)) for row in result]
    
    def count(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count rows"""
        sql = f"SELECT COUNT(*) FROM {table_name}"
        
        if filters:
            conditions = [f"{col} = ?" for col in filters.keys()]
            sql += " WHERE " + " AND ".join(conditions)
            result = self.conn.execute(sql, list(filters.values())).fetchone()[0]
        else:
            result = self.conn.execute(sql).fetchone()[0]
        
        return result
    
    # ==================== UPDATE ====================
    
    def update(self, table_name: str, data: Dict[str, Any], filters: Dict[str, Any]) -> int:
        """Update rows matching filters"""
        update_conditions = [f"{col} = ?" for col in data.keys()]
        where_conditions = [f"{col} = ?" for col in filters.keys()]
        
        sql = f"UPDATE {table_name} SET {', '.join(update_conditions)}"
        sql += f" WHERE {' AND '.join(where_conditions)}"
        
        params = list(data.values()) + list(filters.values())
        self.conn.execute(sql, params)
        return len(data)
    
    def update_by_id(self, table_name: str, id_value: Any, data: Dict[str, Any]) -> int:
        """Update a row by ID"""
        return self.update(table_name, data, {"id": id_value})
    
    # ==================== DELETE ====================
    
    def delete(self, table_name: str, filters: Dict[str, Any]) -> int:
        """Delete rows matching filters"""
        if not filters:
            raise ValueError("Filters required for delete")
        
        conditions = [f"{col} = ?" for col in filters.keys()]
        sql = f"DELETE FROM {table_name} WHERE {' AND '.join(conditions)}"
        
        self.conn.execute(sql, list(filters.values()))
        return len(filters)
    
    def delete_by_id(self, table_name: str, id_value: Any) -> int:
        """Delete a row by ID"""
        return self.delete(table_name, {"id": id_value})
    
    # ==================== TRANSACTION ====================
    
    def begin_transaction(self) -> None:
        self.conn.execute("BEGIN TRANSACTION")
    
    def commit(self) -> None:
        self.conn.execute("COMMIT")
    
    def rollback(self) -> None:
        self.conn.execute("ROLLBACK")

    # ==================== CONTEXT MANAGER ====================
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
